#!/usr/bin/env python3
import json
import re
from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from pprint import pformat, pprint
from typing import Any, Dict, Iterable, List, Set

cycle_dir_pattern = re.compile(r"(?P<t1>Cyc)(?P<cycle>\d+)(?P<t2>_reg)(?P<region>\d+)")
h_and_e_dir_pattern = re.compile(r"(?P<t1>HandE_reg)(?P<region>\d+)")
image_or_bcf_pattern = re.compile(r"(?P<region>\d+)(?P<rest>.+)")

raw_dir = Path("raw")
experiment_json_path = raw_dir / "Experiment.json"
config_txt_path = Path("processed/config.txt")

channel_names_lower = "channelnames.txt"
h_and_e_channel_list = [f"HandE{i}" for i in range(1, 5)]

config_txt_contents = """
radius=6
maxCutoff=0.99
minCutoff=0.05
relativeCutoff=0.2
cell_size_cutoff_factor=0.1
nuclearStainChannel=1
nuclearStainCycle=1
membraneStainChannel=1
membraneStainCycle=-1
use_membrane=false
inner_ring_size=1.0
delaunay_graph=false
anisotropic_region_growth=false
single_plane_quantification=true
""".strip()


def find_codex_datasets(base_dir: Path) -> Iterable[Path]:
    if (base_dir / experiment_json_path).is_file():
        yield base_dir
    for subdir in base_dir.iterdir():
        if (subdir / experiment_json_path).is_file():
            yield subdir


@dataclass
class DatasetFixer:
    dataset_dir: Path
    pretend: bool

    def rename(self, old_path: Path, new_path: Path):
        if self.pretend:
            print("Would rename", old_path, "to", new_path)
        else:
            print("Renaming", old_path, "to", new_path)
            old_path.rename(new_path)

    def fix_image_dir(self, image_dir: Path, region_mapping: Dict[int, int],
                      region_according_to_dir: int):
        for f in image_dir.iterdir():
            if m := image_or_bcf_pattern.match(f.name):
                old_region = int(m.group("region"))

                if old_region in region_mapping:
                    new_region = region_mapping[old_region]
                elif len(region_mapping) == 1 and old_region == 1:
                    new_region = 1
                elif region_according_to_dir == 1:
                    new_region = 1
                else:
                    message = f"Region {old_region} not in region mapping {pformat(region_mapping)} for file {f}, directory {image_dir}"
                    raise ValueError(message)

                if old_region != new_region:
                    new_filename = image_or_bcf_pattern.sub(f"{new_region}\\g<rest>", f.name)
                    new_file_path = f.with_name(new_filename)
                    self.rename(f, new_file_path)

        # TODO: clean up
        if m := cycle_dir_pattern.match(image_dir.name):
            old_region = int(m.group("region"))
            new_region = region_mapping[old_region]
            if old_region != new_region:
                new_dir_name = cycle_dir_pattern.sub(
                    f"\\g<t1>\\g<cycle>\\g<t2>{new_region}", image_dir.name
                )
                new_dir = image_dir.with_name(new_dir_name)
                self.rename(image_dir, new_dir)
        if m := h_and_e_dir_pattern.match(image_dir.name):
            old_region = int(m.group("region"))
            new_region = region_mapping[old_region]
            if old_region != new_region:
                new_dir_name = h_and_e_dir_pattern.sub(f"\\g<t1>{new_region}", image_dir.name)
                new_dir = image_dir.with_name(new_dir_name)
                self.rename(image_dir, new_dir)

    def get_corrected_metadata(self) -> Dict[str, Any]:
        with open(self.dataset_dir / experiment_json_path) as f:
            experiment_metadata = json.load(f)

        dataset_raw_dir = self.dataset_dir / raw_dir
        disk_cycles_by_region = defaultdict(set)
        for child in dataset_raw_dir.iterdir():
            if m := cycle_dir_pattern.match(child.name):
                region = int(m.group("region"))
                cycle = int(m.group("cycle"))
                disk_cycles_by_region[region].add(cycle)

        cycles_intersection: Set[int] = reduce(set.intersection, disk_cycles_by_region.values())
        cycles_union: Set[int] = reduce(set.union, disk_cycles_by_region.values())

        if disparity := cycles_union - cycles_intersection:
            message = f"Found cycles in some regions but not all: {disparity}"
            raise ValueError(message)

        sorted_regions = sorted(disk_cycles_by_region)
        region_mapping = {r: i for i, r in enumerate(sorted_regions, 1)}

        # TODO: fix; just needs to work well enough
        for child in dataset_raw_dir.iterdir():
            if cycle_dir_pattern.match(child.name) or h_and_e_dir_pattern.match(child.name):
                region_according_to_dir = int(cycle_dir_pattern.match(child.name).group("region"))
                self.fix_image_dir(child, region_mapping, region_according_to_dir)

        # need an actual list because we're going to include this
        # in a data structure serialized as JSON
        new_reg_idx = list(range(1, len(sorted_regions) + 1))
        new_reg_names = [f"Region {i}" for i in new_reg_idx]

        experiment_metadata["num_cycles"] = len(cycles_intersection)
        experiment_metadata["cycle_upper_limit"] = max(cycles_intersection)
        experiment_metadata["cycle_lower_limit"] = min(cycles_intersection)
        experiment_metadata["regIdx"] = new_reg_idx
        experiment_metadata["region_names"] = new_reg_names

        return experiment_metadata

    def find_channel_names_file(self) -> Path:
        for f in (self.dataset_dir / "raw").iterdir():
            if f.name.lower() == channel_names_lower:
                return f
        raise ValueError("No channel names file found")

    def get_fixed_channel_names(self, corrected_metadata) -> List[str]:
        with open(self.find_channel_names_file()) as f:
            channel_names = [line.strip() for line in f]

        channels_per_cycle = len(corrected_metadata["channel_names"])
        metadata_channel_count = channels_per_cycle * corrected_metadata["num_cycles"]
        if (
            len(channel_names) == metadata_channel_count + 4
            and channel_names[-4:] == h_and_e_channel_list
        ):
            print("Dropping H&E channels")
            channel_names = channel_names[:-4]

        assert len(channel_names) == metadata_channel_count

        return channel_names

    def fix_dataset(self):
        corrected_metadata = self.get_corrected_metadata()
        corrected_channel_names = self.get_fixed_channel_names(corrected_metadata)

        if self.pretend:
            print("Would fix metadata for", self.dataset_dir)
            pprint(corrected_metadata)
            pprint(corrected_channel_names)
        else:
            experiment_json_file = self.dataset_dir / experiment_json_path
            channel_names_file = self.find_channel_names_file()

            print("Writing new", experiment_json_file)
            with open(experiment_json_file, "w") as f:
                json.dump(corrected_metadata, f, indent=4)

            print("Writing new", channel_names_file)
            with open(channel_names_file, "w") as f:
                for channel in corrected_channel_names:
                    print(channel, file=f)

            if not (config_txt := self.dataset_dir / config_txt_path).is_file():
                print("Writing new", config_txt)
                with open(config_txt, "w") as f:
                    print(config_txt_contents, file=f)


def fix_stanford_codex(base_dir: Path, pretend: bool):
    for dataset_dir in find_codex_datasets(base_dir):
        print(f'fixing {dataset_dir}')
        fixer = DatasetFixer(dataset_dir, pretend)
        fixer.fix_dataset()


if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("directory", type=Path)
    p.add_argument("--pretend", action="store_true")
    args = p.parse_args()

    fix_stanford_codex(args.directory, args.pretend)
