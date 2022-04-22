import argparse
import json
import logging
import re
import traceback
import xml.etree.ElementTree as ET
from glob import glob
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import jsonschema
import numpy as np
import pandas as pd
from packaging import version

from dataset_listing import create_listing_for_each_cycle_region
from schema_container import dataset_schema, get_experiment_metadata_schema


def make_dir_if_not_exists(dir_path: Path):
    if not dir_path.exists():
        dir_path.mkdir(parents=True)


def read_json(path: Path) -> dict:
    with open(path, "r") as s:
        j = json.load(s)
    return j


def read_bool(in_str: str) -> bool:
    if isinstance(in_str, bool):
        return in_str
    if in_str.lower().strip() == "true":
        return True
    else:
        return False


def str_list_to_bools(str_list: List[str]) -> List[bool]:
    return [read_bool(b) for b in str_list]


def np_dtype_to_py_dtype(np_val):
    return np_val.item()


def is_number(in_str: str):
    try:
        float(in_str)
        return True
    except ValueError:
        return False


def read_str(in_str: str) -> str:
    return in_str.strip(",.\r\n\t '\"")


def str_list_strip(str_list: List[str]):
    return [read_str(st) for st in str_list]


def str_list_to_paths(str_list: List[str]):
    return [Path(read_str(p)) for p in str_list]


def read_int_if_can(in_str: str) -> Union[int, str]:
    if isinstance(in_str, int):
        return in_str
    elif isinstance(in_str, float):
        return round(in_str)
    try:
        return round(float(in_str))
    except ValueError:
        return in_str


def get_experiment_json_name(dataset_path: Path) -> str:
    variants = (r"experiment\.json", r"Experiment\.json")
    listing = list(dataset_path.iterdir())
    found = []
    for item in listing:
        for var in variants:
            matched = re.match(var, item.name)
            if matched:
                found.append(matched.string)
    if len(found) > 1:
        msg = "Found several options of experiment file: " + str(variants)
        raise ValueError(msg)
    elif len(found) == 0:
        msg = "File experiment json is not found."
        raise ValueError(msg)
    else:
        return found[0]


def check_other_metadata_present(dataset_path: Path):
    required_files = [
        "segmentation.json",
        "missing1.xlsx",
        "missing2.xlsx",
    ]
    absent_files = []
    for f in required_files:
        fp = dataset_path / f
        if not fp.exists():
            absent_files.append(f)
    if len(absent_files) > 0:
        msg = (
            f"The following required metadata files are absent {str(absent_files)}. "
            + f" These files {str(required_files)}"
            + f" must be present in the specified dataset folder {str(dataset_path)}"
        )
        raise FileNotFoundError(msg)


def alpha_num_order(string: str) -> str:
    """Returns all numbers on 5 digits to let sort the string with numeric order.
    Ex: alpha_num_order("a6b12.125")  ==> "a00006b00012.00125"
    """
    return "".join(
        [
            format(int(x), "05d") if x.isdigit() else x
            for x in re.split(r"(\d+)", string)
        ]
    )


def get_img_dirs(dataset_path: Path) -> List[Path]:
    img_dirs = glob(str(dataset_path / "?yc*_?eg*"))
    if img_dirs == []:
        msg = "No directories with images found. They must follow this pattern cyc001_reg001"
        raise ValueError(msg)
    img_dirs = sorted(img_dirs, key=alpha_num_order)
    img_dirs = [Path(p) for p in img_dirs]
    return img_dirs


def get_img_listing(in_dir: Path) -> List[Path]:
    allowed_extensions = (".tif", ".tiff")
    listing = list(in_dir.iterdir())
    img_listing = [f for f in listing if f.suffix in allowed_extensions]
    img_listing = sorted(img_listing, key=lambda x: alpha_num_order(x.name))
    return img_listing


def extract_keyence_metadata(img_path: Path) -> ET.Element:
    with open(img_path, "r", encoding="utf-8", errors="ignore") as s:
        img_data = s.read()

    # search for xml declaration  '<?xml version="1.0" encoding="utf-8"?>'
    match = re.search(r"<\?xml.*\?>", img_data)
    if match is None:
        msg = "Could not find xml declaration in the TIFF file"
        raise ValueError(msg)

    start = match.span()[0]
    xml_str = img_data[start:]
    xml_data = ET.fromstring(xml_str)
    return xml_data


def get_bin_and_gain(xml_data: ET.Element) -> Tuple[int, int]:
    acq_param = xml_data.find("SingleFileProperty").find("Shooting").find("Parameter")

    gain_db_str = acq_param.find("CameraGain").text
    if is_number(gain_db_str):
        gain_db = int(gain_db_str) // 10
        gain_ratio = round(10 ** (gain_db / 20))
    else:
        msg = "Gain value is not a number"
        raise ValueError(msg)

    binning_str = acq_param.find("Binnin").text
    if binning_str == "Off":
        binning = 1
    elif is_number(binning_str):
        binning = round(float(binning_str))
    else:
        msg = f"Unexpected binning value {binning_str}."
        raise NotImplementedError(msg)
    return binning, gain_ratio


def convert_tiling_mode(tiling_mode: str):
    if "snake" in tiling_mode.lower():
        new_tiling_mode = "Snake"
    elif "grid" in tiling_mode.lower():
        new_tiling_mode = "Grid"
    else:
        raise ValueError("Unknown tiling mode: " + str(tiling_mode))
    return new_tiling_mode


def convert_immersion_medium(imm_med: str):
    imm = imm_med.lower()
    med_types = ("air", "water", "oil", "glycerin")
    for med in med_types:
        if imm in med:
            return med.capitalize()
    else:
        msg = (
            "The immersion medium "
            + imm_med
            + " is not recognized."
            + "The immersion medium must be one of "
            + str(med_types)
        )
        raise ValueError(msg)


class ChannelDetails:
    def __init__(self):
        self.Name = ""
        self.CycleID = 1
        self.ChannelID = 1
        self.Fluorophore = ""
        self.PassedQC = False
        self.QCDetails = ""
        self.ExposureTimeMS = 1
        self.ExcitationWavelengthNM = 1
        self.EmissionWavelengthNM = 1
        self.Binning = 1
        self.Gain = 1


def read_missing2(missing2_meta_path: Path) -> pd.DataFrame:
    fields = [
        "Version",
        "AcquisitionDate",
        "AssayType",
        "AssaySpecificSoftware",
        "AcquisitionMode",
        "DatasetName",
        "MicroscopeName",
    ]

    m2 = pd.read_excel(missing2_meta_path, header=None, index_col=0, usecols=[0, 1])
    m2 = m2.dropna(axis=0)
    clean_index = [read_str(row_name) for row_name in m2.index]

    absent_fields = []
    for f in fields:
        if f not in clean_index:
            absent_fields.append(f)

    if absent_fields != []:
        msg = f"These fields {str(absent_fields)} are absent in the missing2.xlsx"
        raise ValueError(msg)

    m2.index = clean_index
    return m2


def read_missing1(missing1_meta_path: Path, total_num_channels: int) -> pd.DataFrame:
    cols = [
        "Marker",
        "Fluorophore",
        "PassedQC",
        "QCDetails",
        "ExcitationWavelength",
        "EmissionWavelength",
        "IsNuclearMarker",
        "IsMembraneMarker",
    ]
    m1 = pd.read_excel(
        missing1_meta_path, header=0, usecols=cols, dtype=str, nrows=total_num_channels
    )

    if m1.isna().sum().sum() > 0:
        rows_with_missing = m1.index[m1.isna().any(axis=1)]
        rows_with_missing = [r + 1 for r in rows_with_missing]
        msg = (
            "The file missing1.xlsx contains empty or missing values."
            + f" Please check the following rows: {str(rows_with_missing)}"
        )
        raise ValueError(msg)

    for col in cols:
        m1[col] = str_list_strip(m1[col].to_list())

    dtypes = {
        "Marker": str,
        "Fluorophore": str,
        "PassedQC": bool,
        "QCDetails": str,
        "ExcitationWavelength": int,
        "EmissionWavelength": int,
        "IsNuclearMarker": bool,
        "IsMembraneMarker": bool,
    }
    for col, dtype in dtypes.items():
        if dtype is bool:
            m1[col] = str_list_to_bools(m1[col].to_list())
        else:
            m1[col] = m1[col].astype(dtype)
    return m1


def map_segmentation_meta(seg_metadata: dict) -> Dict[str, Dict[str, int]]:
    mapped_seg_meta = {
        "NuclearStainForSegmentation": {
            "CycleID": seg_metadata["nuclearStainCycle"],
            "ChannelID": seg_metadata["nuclearStainChannel"],
        },
        "MembraneStainForSegmentation": {
            "CycleID": seg_metadata["membraneStainCycle"],
            "ChannelID": seg_metadata["membraneStainChannel"],
        },
    }
    return mapped_seg_meta


def map_experiment_meta(exp_metadata: dict) -> Dict[str, Any]:
    ver = exp_metadata["version"]
    if version.parse(ver) >= version.parse("1.7") < version.parse("1.8"):
        bit_depth_key = "bitDepth"
    elif version.parse(ver) >= version.parse("1.5") < version.parse("1.7"):
        bit_depth_key = "bitness"

    mapped_exp_meta = {
        "ImmersionMedium": convert_immersion_medium(exp_metadata["objectiveType"]),
        "NominalMagnification": exp_metadata["magnification"],
        "NumericalAperture": exp_metadata["aperture"],
        "ResolutionX": exp_metadata["xyResolution"],
        "ResolutionXUnit": "nm",
        "ResolutionY": exp_metadata["xyResolution"],
        "ResolutionYUnit": "nm",
        "ResolutionZ": exp_metadata["zPitch"],
        "ResolutionZUnit": "nm",
        "BitDepth": exp_metadata[bit_depth_key],
        "NumRegions": exp_metadata["numRegions"],
        "NumCycles": exp_metadata["numCycles"],
        "NumZPlanes": exp_metadata["numZPlanes"],
        "NumChannels": exp_metadata["numChannels"],
        "RegionWidth": exp_metadata["regionWidth"],
        "RegionHeight": exp_metadata["regionHeight"],
        "TileWidth": exp_metadata["tileWidth"],
        "TileHeight": exp_metadata["tileHeight"],
        "TileOverlapX": exp_metadata["tileOverlapX"],
        "TileOverlapY": exp_metadata["tileOverlapY"],
        "TileLayout": convert_tiling_mode(exp_metadata["tilingMode"]),
    }
    return mapped_exp_meta


def get_nuc_and_membr_markers(
    m1: pd.DataFrame, num_channels_per_cycle: int, seg_meta: dict
) -> Tuple[Dict[str, List[Dict[str, int]]], Dict[str, List[Dict[str, int]]]]:
    nuclear_stain = {"NuclearStain": []}
    membrane_stain = {"MembraneStain": []}
    ch_i = 1
    for i, _id in enumerate(m1.index):
        this_channel_info = m1.loc[_id, :]
        is_nuc_marker = np_dtype_to_py_dtype(this_channel_info["IsNuclearMarker"])
        is_memb_maker = np_dtype_to_py_dtype(this_channel_info["IsMembraneMarker"])

        channel_id = ch_i
        cycle_id = (i // num_channels_per_cycle) + 1

        if is_nuc_marker:
            nuclear_stain["NuclearStain"].append(
                {"CycleID": cycle_id, "ChannelID": channel_id}
            )
        elif is_memb_maker:
            membrane_stain["MembraneStain"].append(
                {"CycleID": cycle_id, "ChannelID": channel_id}
            )

        if ch_i == num_channels_per_cycle:
            ch_i = 1
        else:
            ch_i += 1
    if nuclear_stain["NuclearStain"] == []:
        msg = "Nuclear stain channels is not found in missing1.xlsx"
        raise ValueError(msg)
    if membrane_stain["MembraneStain"] == []:
        msg = "Membrane stain channel is not found in missing1.xlsx"
        raise ValueError(msg)
    if not seg_meta["NuclearStainForSegmentation"] in nuclear_stain["NuclearStain"]:
        msg = "Nuclear stain provided in segmentation.json is not present in missing1.xlsx"
        raise ValueError(msg)
    if not seg_meta["MembraneStainForSegmentation"] in membrane_stain["MembraneStain"]:
        msg = "Membrane stain provided in segmentation.json is not present in missing1.xlsx"
        raise ValueError(msg)
    return nuclear_stain, membrane_stain


def read_exposure_times_table(
    exposure_times_table_path: Path,
) -> Union[None, List[List[Union[str, int]]]]:
    if not exposure_times_table_path.exists():
        return None
    exp_times = pd.read_csv(exposure_times_table_path, header=None)
    exposure_times = []
    for row in range(0, len(exp_times)):
        this_cycle_exposure = exp_times.loc[row, :].to_list()
        this_cycle_exposure = [read_int_if_can(t) for t in this_cycle_exposure]
        exposure_times.append(this_cycle_exposure)
    return exposure_times


def get_exposure_times(
    exp_metadata: dict, exposure_times_table: Union[None, pd.DataFrame] = None
) -> List[List[Union[str, int]]]:
    if exp_metadata.get("exposureTimes", None) is not None:
        exposure_times = exp_metadata["exposureTimes"]["exposureTimesArray"]
    else:
        if exposure_times_table is not None:
            exposure_times = exposure_times_table
        else:
            msg = (
                "Tried to look in the experiment.json and exposure_times.txt"
                + " But did not find exposure time information."
            )
            raise ValueError(msg)
    return exposure_times


def create_channel_details(
    m1: pd.DataFrame,
    bin_list: List[int],
    gain_list: List[int],
    exposure_times: List[List[str]],
    num_channels_per_cycle: int,
) -> List[ChannelDetails]:
    channel_list = []
    n = 0
    ch_i = 1
    for i, _id in enumerate(m1.index):
        this_channel_info = m1.loc[_id, :]

        channel_id = ch_i
        cycle_id = (i // num_channels_per_cycle) + 1

        ch = ChannelDetails()
        ch.Name = this_channel_info["Marker"]
        ch.ChannelID = channel_id
        ch.CycleID = cycle_id
        ch.Fluorophore = this_channel_info["Fluorophore"]
        ch.PassedQC = np_dtype_to_py_dtype(this_channel_info["PassedQC"])
        ch.QCDetails = this_channel_info["QCDetails"]
        ch.ExcitationWavelengthNM = np_dtype_to_py_dtype(
            this_channel_info["ExcitationWavelength"]
        )
        ch.EmissionWavelengthNM = np_dtype_to_py_dtype(
            this_channel_info["EmissionWavelength"]
        )

        cycle_info = exposure_times[ch.CycleID]
        exposure_time = int(cycle_info[ch.ChannelID])
        ch.ExposureTimeMS = exposure_time
        ch.Binning = bin_list[n]
        ch.Gain = gain_list[n]

        if ch_i == num_channels_per_cycle:
            ch_i = 1
        else:
            ch_i += 1
        n += 1
        channel_list.append(ch)
    return channel_list


def get_bin_gain_from_embedded_meta(listing: dict) -> Tuple[List[int], List[int]]:
    bin_list = []
    gain_list = []
    for cyc in listing:
        reg = list(listing[cyc].keys())[0]
        for ch in listing[cyc][reg]:
            # take only first zplane of the first tile to get bin and gain
            ti = list(listing[cyc][reg][ch].keys())[0]
            # values are paths to each zplane
            img_path = list(listing[cyc][reg][ch][ti].values())[0]

            xml_data = extract_keyence_metadata(img_path)
            binning, gain = get_bin_and_gain(xml_data)
            bin_list.append(binning)
            gain_list.append(gain)
    return bin_list, gain_list


def map_missing2(m2):
    m2_data = m2.to_dict()[1]  # col 0 mapped to index, and col 1 contains the info
    mapped_missing2_meta = {
        "Version": m2_data["Version"],
        "AcquisitionDate": m2_data["AcquisitionDate"],
        "AssayType": m2_data["AssayType"],
        "AssaySpecificSoftware": m2_data["AssaySpecificSoftware"],
        "AcquisitionMode": m2_data["AcquisitionMode"],
        "DatasetName": m2_data["DatasetName"],
        "Microscope": m2_data["MicroscopeName"],
    }
    return mapped_missing2_meta


def check_listing_to_metadata_cor(listing: dict, exp_metadata: dict):
    msg_t = "Number of {smth} is different from the one specified in the metadata."
    cyc_t = msg_t.format(smth="cycles") + " Expected {exp}, got {got}."
    reg_t = msg_t.format(smth="regions in cycle {cyc}") + " Expected {exp}, got {got}."
    ch_t = (
        msg_t.format(smth="channels in cycle {cyc}, region {reg}")
        + " Expected {exp}, got {got}."
    )
    ti_t = (
        msg_t.format(smth="tiles in cycle {cyc}, region {reg}, channel {ch}")
        + " Expected {exp}, got {got}."
    )
    zp_t = (
        msg_t.format(
            smth="zplanes in cycle {cyc}, region {reg}, channel {ch}, tile {ti}"
        )
        + " Expected {exp}, got {got}."
    )

    assert len(listing.keys()) == exp_metadata["NumCycles"], cyc_t.format(
        exp=exp_metadata["NumCycles"], got=len(listing.keys())
    )
    for cyc in listing:
        regions = listing[cyc].keys()
        assert len(regions) == exp_metadata["NumRegions"], reg_t.format(
            cyc=cyc, exp=exp_metadata["NumRegions"], got=len(regions)
        )
        for reg in regions:
            channels = listing[cyc][reg].keys()
            assert len(channels) == exp_metadata["NumChannels"], ch_t.format(
                cyc=cyc, reg=reg, exp=exp_metadata["NumChannels"], got=len(channels)
            )
            for ch in channels:
                tiles = listing[cyc][reg][ch].keys()
                num_tiles = exp_metadata["RegionWidth"] * exp_metadata["RegionHeight"]
                assert len(tiles) == num_tiles, ti_t.format(
                    cyc=cyc, reg=reg, ch=ch, exp=num_tiles, got=len(tiles)
                )
                for ti in tiles:
                    zplanes = listing[cyc][reg][ch][ti].keys()
                    assert len(zplanes) == exp_metadata["NumZPlanes"], zp_t.format(
                        cyc=cyc,
                        reg=reg,
                        ch=ch,
                        ti=ti,
                        exp=exp_metadata["NumZPlanes"],
                        got=len(zplanes),
                    )


def convert_metadata(dataset_path: Path, out_path: Path):
    if not dataset_path.exists():
        msg = f"Specified input directory {dataset_path} does not exist"
        raise FileNotFoundError(msg)
    if not out_path.exists():
        logger.info(f"Output directory {out_path} does not exist. Will create new.")
        make_dir_if_not_exists(out_path)

    experiment_json_name = get_experiment_json_name(dataset_path)
    check_other_metadata_present(dataset_path)

    exp_path = dataset_path / experiment_json_name
    seg_path = dataset_path / "segmentation.json"
    missing1_meta_path = dataset_path / "missing1.xlsx"
    missing2_meta_path = dataset_path / "missing2.xlsx"
    exposure_times_table_path = dataset_path / "exposure_times.txt"

    exp_metadata = read_json(exp_path)
    seg_metadata = read_json(seg_path)

    logger.debug("Reading experiment data")

    experiment_schema = get_experiment_metadata_schema(exp_metadata)
    jsonschema.validate(exp_metadata, experiment_schema)
    mapped_exp_meta = map_experiment_meta(exp_metadata)
    mapped_seg_meta = map_segmentation_meta(seg_metadata)

    exposure_times_table = read_exposure_times_table(exposure_times_table_path)
    exposure_times = get_exposure_times(exp_metadata, exposure_times_table)

    total_num_channels = mapped_exp_meta["NumCycles"] * mapped_exp_meta["NumChannels"]
    num_channels_per_cycle = mapped_exp_meta["NumChannels"]

    logger.debug("Reading missing data")
    m1 = read_missing1(missing1_meta_path, total_num_channels)
    m2 = read_missing2(missing2_meta_path)
    mapped_missing2_meta = map_missing2(m2)

    logger.debug("Reading data embedded in images")
    img_dirs = get_img_dirs(dataset_path)
    listing = create_listing_for_each_cycle_region(img_dirs)
    check_listing_to_metadata_cor(listing, mapped_exp_meta)
    bin_list, gain_list = get_bin_gain_from_embedded_meta(listing)

    logger.debug("Populating ChannelDetails")

    nuclear_stain, membrane_stain = get_nuc_and_membr_markers(
        m1, num_channels_per_cycle, mapped_seg_meta
    )

    channel_list = create_channel_details(
        m1, bin_list, gain_list, exposure_times, num_channels_per_cycle
    )
    channel_metadata = {
        "ChannelDetails": {"ChannelDetailsArray": [ch.__dict__ for ch in channel_list]}
    }

    logger.debug("Combining collected metadata")
    metadata_dicts = (
        mapped_missing2_meta,
        mapped_exp_meta,
        nuclear_stain,
        membrane_stain,
        mapped_seg_meta,
        channel_metadata,
    )

    complete_metadata = dict()
    for dictionary in metadata_dicts:
        for k, v in dictionary.items():
            complete_metadata[k] = v

    logger.debug("Validating collected metadata")
    jsonschema.validate(complete_metadata, dataset_schema)
    logger.debug("Writing final dataset.json")
    with open(out_path / "dataset.json", "w", encoding="utf-8") as s:
        json.dump(complete_metadata, s, indent=4, sort_keys=False)
    return


def read_input_excel(workdir) -> Dict[Path, Path]:
    input_path = workdir / "input.xlsx"

    if not input_path.exists():
        msg = (
            "The input.xlsx file is not found. "
            + f"Please put it into this directory {str(workdir)}."
        )
        raise FileNotFoundError(msg)

    input_map = pd.read_excel(input_path, header=0, usecols=[0, 1], dtype=str)
    input_map = input_map.dropna(axis=0)

    inputs = str_list_to_paths(input_map["InputDir"].to_list())
    outputs = str_list_to_paths(input_map["OutputDir"].to_list())
    input_output_map = {i: o for i, o in zip(inputs, outputs)}
    return input_output_map


def main(workdir: Path):
    input_output_map = read_input_excel(workdir)
    collected_exceptions = []
    logger.info("Started conversion")

    for input_dir, out_dir in input_output_map.items():
        logger.info("Converting metadata in dataset " + str(input_dir))
        try:
            convert_metadata(input_dir, out_dir)
            logger.info("Success")
            logger.info("\n")
        except Exception as e:
            tr = traceback.format_exc()
            collected_exceptions.append((input_dir, e, tr))
            logger.info("Failed")
            logger.info("\n")

    num_total = len(input_output_map.keys())
    num_failed = len(collected_exceptions)
    logger.info("REPORT:")
    if num_failed > 0:
        logger.info("Conversion failed for the following datasets, with errors:")
        for ex in collected_exceptions:
            logger.info("Dataset: " + str(ex[0]))
            logger.info("Error: " + str(ex[1]))
            logger.debug("Traceback: " + str(ex[2]))
            logger.info("\n")
    logger.info(
        "Successfully converted datasets "
        + str(num_total - num_failed)
        + "/"
        + str(num_total)
    )
    logger.info("FINISHED")
    _ = input("Press Enter to close")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--workdir", type=Path, help="dir where input.xlsx is stored")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(args.workdir / "log.log")
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)
    log_format = "%(asctime)s - %(levelname)s: %(message)s"
    datefmt = "%H:%M:%S"
    c_format = logging.Formatter(log_format, datefmt=datefmt)
    f_format = logging.Formatter(log_format, datefmt=datefmt)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info("\n")
    logger.info("STARTED")

    main(args.workdir)
