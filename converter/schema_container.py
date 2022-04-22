import json

from packaging import version

_dataset_schema_str = """{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "Version": "1.0",
            "DatasetName": "Some recognizable name",
            "AcquisitionDate": "2020-02-19T13:51:35.857-05:00[America/New_York]",
            "AssayType": "CODEX",
            "AssaySpecificSoftware": "Akoya CODEX Instrument Manager 1.29, Akoya CODEX Processor 1.7.6",
            "Microscope": "Sony, Nikon, Zeiss",
            "AcquisitionMode": "Confocal",
            "ImmersionMedium": "Air",
            "NominalMagnification": 40,
            "NumericalAperture": 1.0,
            "ResolutionX": 300,
            "ResolutionXUnit": "nm",
            "ResolutionY": 300,
            "ResolutionYUnit": "nm",
            "ResolutionZ": 100,
            "ResolutionZUnit": "nm",
            "BitDepth": 16,
            "NumRegions": 3,
            "NumCycles": 4,
            "NumZPlanes": 5,
            "NumChannels": 6,
            "RegionWidth": 10,
            "RegionHeight": 10,
            "TileWidth": 2048,
            "TileHeight": 2048,
            "TileOverlapX": 0.3,
            "TileOverlapY": 0.3,
            "TileLayout": "snake",
            "NuclearStain": [
                {"CycleID": 2, "ChannelID": 1}
            ],
            "MembraneStain": [
                {"CycleID": 2, "ChannelID": 3},
                {"CycleID": 3, "ChannelID": 4}
            ],
            "NuclearStainForSegmentation": {"CycleID": 2, "ChannelID": 1},
            "MembraneStainForSegmentation": {"CycleID": 3, "ChannelID": 4},
            "ChannelDetails": {
                "ChannelDetailsArray": [
                    {
                        "Name": "DAPI-01",
                        "ChannelID": 1,
                        "CycleID": 1,
                        "Fluorophore": "DAPI",
                        "PassedQC": true,
                        "QCDetails": "if QC failed why",
                        "ExposureTimeMS": 10.0,
                        "ExcitationWavelengthNM": 350,
                        "EmissionWavelengthNM": 450,
                        "Binning": 1,
                        "Gain": 1.0
                    },
                    {
                        "Name": "CD31",
                        "ChannelID": 2,
                        "CycleID": 1,
                        "Fluorophore": "Cy5",
                        "PassedQC": true,
                        "QCDetails": "None",
                        "ExposureTimeMS": 100.0,
                        "ExcitationWavelengthNM": 650,
                        "EmissionWavelengthNM": 660,
                        "Binning": 1,
                        "Gain": 1.0
                    }
                ]
            }
        }
    ],
    "required": [
        "Version",
        "DatasetName",
        "AcquisitionDate",
        "AssayType",
        "AssaySpecificSoftware",
        "Microscope",
        "AcquisitionMode",
        "ImmersionMedium",
        "NominalMagnification",
        "NumericalAperture",
        "ResolutionX",
        "ResolutionXUnit",
        "ResolutionY",
        "ResolutionYUnit",
        "ResolutionZ",
        "ResolutionZUnit",
        "BitDepth",
        "NumRegions",
        "NumCycles",
        "NumZPlanes",
        "NumChannels",
        "RegionWidth",
        "RegionHeight",
        "TileWidth",
        "TileHeight",
        "TileOverlapX",
        "TileOverlapY",
        "TileLayout",
        "NuclearStain",
        "MembraneStain",
        "NuclearStainForSegmentation",
        "MembraneStainForSegmentation",
        "ChannelDetails"
    ],
    "properties": {
        "Version": {
            "$id": "#/properties/Version",
            "type": "string",
            "title": "The Version schema",
            "description": "The version of CODEX metadata.",
            "default": "1.0",
            "examples": [
                "1.0"
            ]
        },
        "DatasetName": {
            "$id": "#/properties/DatasetName",
            "type": "string",
            "title": "The DatasetName schema",
            "description": "Name of the CODEX dataset recognizable by the data provider.",
            "default": "None",
            "examples": [
                "Some recognizable name"
            ]
        },
        "AcquisitionDate": {
            "$id": "#/properties/AcquisitionDate",
            "type": "string",
            "title": "The AcquisitionDate schema",
            "description": "Dataset acquisition date.",
            "default": "None",
            "examples": [
                "2020-02-19T13:51:35.857-05:00[America/New_York]"
            ]
        },
        "AssayType": {
            "$id": "#/properties/AssayType",
            "type": "string",
            "title": "The AssayType schema",
            "enum": ["CODEX", "ImmunoSABER"],
            "description": "The type of the assay.",
            "default": "None",
            "examples": [
                "CODEX"
            ]
        },
        "AssaySpecificSoftware": {
            "$id": "#/properties/AssaySpecificSoftware",
            "type": "string",
            "title": "The AssaySpecificSoftware schema",
            "description": "The comma separated list of company, name and version of the assay specific software used for this dataset.",
            "default": "None",
            "examples": [
                "Akoya CODEX Instrument Manager 1.29, Akoya CODEX Processor 1.7.6 "
            ]
        },
        "Microscope": {
            "$id": "#/properties/Microscope",
            "type": "string",
            "title": "The Microscope schema",
            "description": "Details about the microscope manufacturer and the model.",
            "default": "None",
            "examples": [
                "Sony, Nikon, Zeiss"
            ]
        },
        "AcquisitionMode": {
            "$id": "#/properties/AcquisitionMode",
            "type": "string",
            "enum": ["Confocal", "WideField", "Lightsheet", "SingleMolecule",
                     "MultiPhoton", "StructuredIllumination", "Spectral",
                     "TotalInternalReflection", "BrightField"],
            "title": "The AcquisitionMode schema",
            "description": "Type of the microscopy method.",
            "default": "Confocal",
            "examples": [
                "Confocal"
            ]
        },
        "ImmersionMedium": {
            "$id": "#/properties/ImmersionMedium",
            "type": "string",
            "enum": ["Air", "Water", "Oil", "Glycerin"],
            "title": "The ImmersionMedium schema",
            "description": "Type of the objective immersion medium.",
            "default": "Air",
            "examples": [
                "Air"
            ]
        },
        "NominalMagnification": {
            "$id": "#/properties/NominalMagnification",
            "type": "number",
            "minimum": 0.0,
            "title": "The NominalMagnification schema",
            "description": "The magnification of the objective as specified by the manufacturer.",
            "default": 40,
            "examples": [
                40
            ]
        },
        "NumericalAperture": {
            "$id": "#/properties/NumericalAperture",
            "type": "number",
            "minimum": 0.1,
            "title": "The NumericalAperture schema",
            "description": "The numerical aperture of the objective.",
            "default": 0.1,
            "examples": [
                1.0
            ]
        },
        "ResolutionX": {
            "$id": "#/properties/ResolutionX",
            "type": "number",
            "minimum": 0.0,
            "title": "The ResolutionX schema",
            "description": "Physical size of a pixel.",
            "default": 0.0,
            "examples": [
                300.0
            ]
        },
        "ResolutionXUnit": {
            "$id": "#/properties/ResolutionXUnit",
            "type": "string",
            "enum": ["m", "dm", "cm", "mm", "um", "nm", "pm", "fm"],
            "title": "The ResolutionXUnit schema",
            "description": "The units of the physical size of a pixel.",
            "default": "nm",
            "examples": [
                "nm"
            ]
        },
        "ResolutionY": {
            "$id": "#/properties/ResolutionY",
            "type": "number",
            "minimum": 0.0,
            "title": "The ResolutionY schema",
            "description": "Physical size of a pixel.",
            "default": 0.0,
            "examples": [
                300.0
            ]
        },
        "ResolutionYUnit": {
            "$id": "#/properties/ResolutionYUnit",
            "type": "string",
            "enum": ["m", "dm", "cm", "mm", "um", "nm", "pm", "fm"],
            "title": "The ResolutionYUnit schema",
            "description": "The units of the physical size of a pixel.",
            "default": "nm",
            "examples": [
                "nm"
            ]
        },
        "ResolutionZ": {
            "$id": "#/properties/ResolutionZ",
            "type": "number",
            "minimum": 0.0,
            "title": "The ResolutionZ schema",
            "description": "Physical size of a pixel.",
            "default": 0.0,
            "examples": [
                100.0
            ]
        },
        "ResolutionZUnit": {
            "$id": "#/properties/ResolutionZUnit",
            "type": "string",
            "enum": ["m", "dm", "cm", "mm", "um", "nm", "pm", "fm"],
            "title": "The ResolutionZUnit schema",
            "description": "The units of the physical size of a pixel.",
            "default": "nm",
            "examples": [
                "nm"
            ]
        },
        "BitDepth": {
            "$id": "#/properties/BitDepth",
            "type": "integer",
            "multipleOf": 2,
            "title": "The BitDepth schema",
            "description": "Size of the tile horizontal direction in pixels of bits per pixel.",
            "default": 16,
            "examples": [
                16
            ]
        },

        "NumRegions": {
            "$id": "#/properties/NumRegions",
            "type": "integer",
            "minimum": 1,
            "title": "The NumRegions schema",
            "description": "The number of regions in the dataset.",
            "default": 1,
            "examples": [
                3
            ]
        },
        "NumCycles": {
            "$id": "#/properties/NumCycles",
            "type": "integer",
            "minimum": 1,
            "title": "The NumCycles schema",
            "description": "The number of cycles in the dataset.",
            "default": 1,
            "examples": [
                4
            ]
        },
        "NumZPlanes": {
            "$id": "#/properties/NumZPlanes",
            "type": "integer",
            "minimum": 1,
            "title": "The NumZPlanes schema",
            "description": "The number of focal planes captured.",
            "default": 1,
            "examples": [
                5
            ]
        },
        "NumChannels": {
            "$id": "#/properties/NumChannels",
            "type": "integer",
            "minimum": 1,
            "title": "The NumChannels schema",
            "description": "The number of imaging channels captured.",
            "default": 1,
            "examples": [
                6
            ]
        },
        "RegionWidth": {
            "$id": "#/properties/RegionWidth",
            "type": "integer",
            "minimum": 1,
            "title": "The RegionWidth schema",
            "description": "The number of tiles per region in horizontal direction.",
            "default": 1,
            "examples": [
                10
            ]
        },
        "RegionHeight": {
            "$id": "#/properties/RegionHeight",
            "type": "integer",
            "minimum": 1,
            "title": "The RegionHeight schema",
            "description": "The number of tiles per region in vertical direction.",
            "default": 1,
            "examples": [
                10
            ]
        },
        "TileWidth": {
            "$id": "#/properties/TileWidth",
            "type": "integer",
            "minimum": 1,
            "title": "The TileWidth schema",
            "description": "The size of a tile horizontal direction in pixels.",
            "default": 1,
            "examples": [
                2048
            ]
        },
        "TileHeight": {
            "$id": "#/properties/TileHeight",
            "type": "integer",
            "minimum": 1,
            "title": "The TileHeight schema",
            "description": "The size of a tile vertical direction in pixels.",
            "default": 1,
            "examples": [
                2048
            ]
        },
        "TileOverlapX": {
            "$id": "#/properties/TileOverlapX",
            "type": "number",
            "minimum": 0.0,
            "exclusiveMaximum": 1.0,
            "title": "The TileOverlapX schema",
            "description": "The horizontal overlap between neighbouring tiles in fractions of one.",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "TileOverlapY": {
            "$id": "#/properties/TileOverlapY",
            "type": "number",
            "minimum": 0.0,
            "exclusiveMaximum": 1.0,
            "title": "The TileOverlapY schema",
            "description": "The vertical overlap between neighbouring tiles in fractions of one.",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "TileLayout": {
            "$id": "#/properties/TileLayout",
            "type": "string",
            "enum": ["Snake", "Grid"],
            "title": "The TileLayout schema",
            "description": "The way tiles are captured by the microscope.",
            "default": "Snake",
            "examples": [
                "Snake"
            ]
        },
        "NuclearStain": {
            "$id": "#/properties/NuclearStain",
            "type": "array",
            "title": "The NuclearStain schema",
            "minItems": 1,
            "uniqueItems": true,
            "description": "A list of cycle and channel ids that capture stained nuclei.",
            "default": [],
            "examples": [
                [
                    {
                        "CycleID": 1,
                        "ChannelID": 1
                    }
                ]
            ],
            "additionalItems": true,
            "items": {
                "$id": "#/properties/NuclearStain/items",
                "allOf": [
                    {
                        "$id": "#/properties/NuclearStain/items/allOf/0",
                        "type": "object",
                        "title": "The first allOf schema",
                        "description": "The cycle and channel ids that capture stained nuclei.",
                        "default": {},
                        "examples": [
                            {
                                "CycleID": 1,
                                "ChannelID": 1
                            }
                        ],
                        "required": [
                            "CycleID",
                            "ChannelID"
                        ],
                        "properties": {
                            "CycleID": {
                                "$id": "#/properties/NuclearStain/items/allOf/0/properties/CycleID",
                                "type": "integer",
                                "minimum": 1,
                                "title": "The Cycle schema",
                                "description": "The id of the cycle from which to use nuclear stain.",
                                "default": 1,
                                "examples": [
                                    1
                                ]
                            },
                            "ChannelID": {
                                "$id": "#/properties/NuclearStain/items/allOf/0/properties/ChannelID",
                                "type": "integer",
                                "minimum": 1,
                                "title": "The Channel schema",
                                "description": "The id of the channel, inside the cycle, that captures stained nuclei.",
                                "default": 1,
                                "examples": [
                                    1
                                ]
                            }
                        },
                        "additionalProperties": true
                    }
                ]
            }
        },
        "MembraneStain": {
            "$id": "#/properties/MembraneStain",
            "type": "array",
            "minItems": 1,
            "uniqueItems": true,
            "title": "The MembraneStain schema",
            "description": "A list of cycle and channel ids that capture stained cell membranes.",
            "default": [],
            "examples": [
                [
                    {
                        "CycleID": 2,
                        "ChannelID": 3
                    },
                    {
                        "CycleID": 3,
                        "ChannelID": 4
                    }
                ]
            ],
            "additionalItems": true,
            "items": {
                "$id": "#/properties/MembraneStain/items",
                "allOf": [
                    {
                        "$id": "#/properties/MembraneStain/items/allOf/0",
                        "type": "object",
                        "title": "The first allOf schema",
                        "description": "The cycle and channel ids that capture stained cell membranes.",
                        "default": {},
                        "examples": [
                            {
                                "CycleID": 2,
                                "ChannelID": 3
                            }
                        ],
                        "required": [
                            "CycleID",
                            "ChannelID"
                        ],
                        "properties": {
                            "CycleID": {
                                "$id": "#/properties/MembraneStain/items/allOf/0/properties/CycleID",
                                "type": "integer",
                                "minimum": 1,
                                "title": "The Cycle schema",
                                "description": "The id of the cycle that captures stained cell membranes.",
                                "default": 1,
                                "examples": [
                                    2
                                ]
                            },
                            "ChannelID": {
                                "$id": "#/properties/MembraneStain/items/allOf/0/properties/ChannelID",
                                "type": "integer",
                                "minimum": 1,
                                "title": "The Channel schema",
                                "description": "The id of the channel that captures stained cell membranes.",
                                "default": 1,
                                "examples": [
                                    3
                                ]
                            }
                        },
                        "additionalProperties": true
                    }
                ]
            }
        },
        "NuclearStainForSegmentation": {
            "$id": "#/properties/NuclearStainForSegmentation",
            "type": "object",
            "title": "The NuclearStainForSegmentation schema",
            "description": "The cycle and channel ids that will be used for nuclear segmentation.",
            "default": {},
            "examples": [
                {
                    "CycleID": 2,
                    "ChannelID": 1
                }
            ],
            "required": [
                "CycleID",
                "ChannelID"
            ],
            "properties": {
                "CycleID": {
                    "$id": "#/properties/NuclearStainForSegmentation/properties/CycleID",
                    "type": "integer",
                    "minimum": 1,
                    "title": "The Cycle schema",
                    "description": "The cycle id that will be used for nuclear segmentation.",
                    "default": 1,
                    "examples": [
                        2
                    ]
                },
                "ChannelID": {
                    "$id": "#/properties/NuclearStainForSegmentation/properties/ChannelID",
                    "type": "integer",
                    "minimum": 1,
                    "title": "The Channel schema",
                    "description": "The channel id, inside the cycle, that will be used for nuclear segmentation.",
                    "default": 1,
                    "examples": [
                        1
                    ]
                }
            },
            "additionalProperties": true
        },
        "MembraneStainForSegmentation": {
            "$id": "#/properties/MembraneStainForSegmentation",
            "type": "object",
            "title": "The MembraneStainForSegmentation schema",
            "description": "The cycle and channel ids that will be used for cell segmentation.",
            "default": {},
            "examples": [
                {
                    "CycleID": 3,
                    "ChannelID": 4
                }
            ],
            "required": [
                "CycleID",
                "ChannelID"
            ],
            "properties": {
                "CycleID": {
                    "$id": "#/properties/MembraneStainForSegmentation/properties/CycleID",
                    "type": "integer",
                    "minimum": 1,
                    "title": "The Cycle schema",
                    "description": "The cycle id that will be used for cell segmentation.",
                    "default": 1,
                    "examples": [
                        3
                    ]
                },
                "ChannelID": {
                    "$id": "#/properties/MembraneStainForSegmentation/properties/ChannelID",
                    "type": "integer",
                    "minimum": 1,
                    "title": "The Channel schema",
                    "description": "The channel id, inside the cycle, that will be used for cell segmentation.",
                    "default": 1,
                    "examples": [
                        4
                    ]
                }
            },
            "additionalProperties": true
        },
        "ChannelDetails": {
            "$id": "#/properties/ChannelDetails",
            "type": "object",
            "title": "The ChannelDetails schema",
            "description": "The acquisition details for each imaging channel.",
            "default": {},
            "examples": [
                {
                    "ChannelDetailsArray": [
                        {
                            "Name": "DAPI-01",
                            "ChannelID": 1,
                            "CycleID": 1,
                            "Fluorophore": "DAPI",
                            "PassedQC": true,
                            "QCDetails": "if QC failed why",
                            "ExposureTimeMS": 10.0,
                            "ExcitationWavelengthNM": 350,
                            "EmissionWavelengthNM": 450,
                            "Binning": 1,
                            "Gain": 1.0
                        },
                        {
                            "Name": "CD31",
                            "ChannelID": 2,
                            "CycleID": 1,
                            "Fluorophore": "Cy5",
                            "PassedQC": true,
                            "QCDetails": "None",
                            "ExposureTimeMS": 100.0,
                            "ExcitationWavelengthNM": 650,
                            "EmissionWavelengthNM": 660,
                            "Binning": 1,
                            "Gain": 1.0
                        }
                    ]
                }
            ],
            "required": [
                "ChannelDetailsArray"
            ],
            "properties": {
                "ChannelDetailsArray": {
                    "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray",
                    "type": "array",
                    "minItems": 1,
                    "uniqueItems": true,
                    "title": "The ChannelDetailsArray schema",
                    "description": "An explanation about the purpose of this instance.",
                    "default": [],
                    "examples": [
                        [
                            {
                                "Name": "DAPI-01",
                                "ChannelID": 1,
                                "CycleID": 1,
                                "Fluorophore": "DAPI",
                                "PassedQC": true,
                                "QCDetails": "if QC failed why",
                                "ExposureTimeMS": 10.0,
                                "ExcitationWavelengthNM": 350,
                                "EmissionWavelengthNM": 450,
                                "Binning": 1,
                                "Gain": 1.0
                            },
                            {
                                "Name": "CD31",
                                "ChannelID": 2,
                                "CycleID": 1,
                                "Fluorophore": "Cy5",
                                "PassedQC": true,
                                "QCDetails": "None",
                                "ExposureTimeMS": 100.0,
                                "ExcitationWavelengthNM": 650,
                                "EmissionWavelengthNM": 660,
                                "Binning": 1,
                                "Gain": 1.0
                            }
                        ]
                    ],
                    "additionalItems": true,
                    "items": {
                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items",
                        "allOf": [
                            {
                                "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0",
                                "type": "object",
                                "title": "The first allOf schema",
                                "description": "An explanation about the purpose of this instance.",
                                "default": {},
                                "examples": [
                                    {
                                        "Name": "DAPI-01",
                                        "ChannelID": 1,
                                        "CycleID": 1,
                                        "Fluorophore": "DAPI",
                                        "PassedQC": true,
                                        "QCDetails": "if QC failed why",
                                        "ExposureTimeMS": 10.0,
                                        "ExcitationWavelengthNM": 350,
                                        "EmissionWavelengthNM": 450,
                                        "Binning": 1,
                                        "Gain": 1.0
                                    }
                                ],
                                "required": [
                                    "Name",
                                    "ChannelID",
                                    "CycleID",
                                    "Fluorophore",
                                    "PassedQC",
                                    "QCDetails",
                                    "ExposureTimeMS",
                                    "ExcitationWavelengthNM",
                                    "EmissionWavelengthNM",
                                    "Binning",
                                    "Gain"
                                ],
                                "properties": {
                                    "Name": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/Name",
                                        "type": "string",
                                        "title": "The Name schema",
                                        "description": "The name of the channel or its target.",
                                        "default": "None",
                                        "examples": [
                                            "DAPI-01"
                                        ]
                                    },
                                    "ChannelID": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/ChannelID",
                                        "type": "integer",
                                        "minimum": 1,
                                        "title": "The ChannelID schema",
                                        "description": "The id of the imaging channel inside the cycle.",
                                        "default": 1,
                                        "examples": [
                                            1
                                        ]
                                    },
                                    "CycleID": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/CycleID",
                                        "type": "integer",
                                        "minimum": 1,
                                        "title": "The CycleID schema",
                                        "description": "The id of the imaging cycle.",
                                        "default": 1,
                                        "examples": [
                                            1
                                        ]
                                    },
                                    "Fluorophore": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/Fluorophore",
                                        "type": "string",
                                        "title": "The Fluorophore schema",
                                        "description": "The name of the fluorophore for this channel.",
                                        "default": "None",
                                        "examples": [
                                            "DAPI"
                                        ]
                                    },
                                    "PassedQC": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/PassedQC",
                                        "type": "boolean",
                                        "title": "The PassedQC schema",
                                        "description": "Check if the channel passed qc.",
                                        "default": true,
                                        "examples": [
                                            true
                                        ]
                                    },
                                    "QCDetails": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/QCDetails",
                                        "type": "string",
                                        "title": "The QCDetails schema",
                                        "description": "Additional details about qc.",
                                        "default": "None",
                                        "examples": [
                                            "if QC failed why"
                                        ]
                                    },
                                    "ExposureTimeMS": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/ExposureTimeMS",
                                        "type": "number",
                                        "minimum": 0.0,
                                        "title": "The ExposureTimeMS schema",
                                        "description": "The length of the exposure in milliseconds.",
                                        "default": 0.0,
                                        "examples": [
                                            10.0
                                        ]
                                    },
                                    "ExcitationWavelengthNM": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/ExcitationWavelengthNM",
                                        "type": "integer",
                                        "minimum": 1,
                                        "title": "The ExcitationWavelengthNM schema",
                                        "description": "The wavelength of light absorption by a fluorophore in nanometers.",
                                        "default": 1,
                                        "examples": [
                                            350
                                        ]
                                    },
                                    "EmissionWavelengthNM": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/EmissionWavelengthNM",
                                        "type": "integer",
                                        "minimum": 1,
                                        "title": "The EmissionWavelengthNM schema",
                                        "description": "The wavelength of light emission by a fluorophore in nanometers.",
                                        "default": 1,
                                        "examples": [
                                            450
                                        ]
                                    },
                                    "Binning": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/Binning",
                                        "type": "integer",
                                        "minimum": 1,
                                        "title": "The Binning schema",
                                        "description": "The number of pixels that are combined during or after detection.",
                                        "default": 1,
                                        "examples": [
                                            1
                                        ]
                                    },
                                     "Gain": {
                                        "$id": "#/properties/ChannelDetails/properties/ChannelDetailsArray/items/allOf/0/properties/Gain",
                                        "type": "number",
                                        "minimum": 1.0,
                                        "title": "The Gain schema",
                                        "description": "Amplification applied to the detector signal.",
                                        "default": 1.0,
                                        "examples": [
                                            1.0
                                        ]
                                    }
                                },
                                "additionalProperties": true
                            }
                        ]
                    }
                }
            },
            "additionalProperties": true
        }
    },
    "additionalProperties": true
}
"""

_experiment_1_7_schema_str = """{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "version": "1.7.0.6",
            "name": "src_CX_19-002_CC2-spleen-A",
            "runName": "2020-02-10",
            "dateProcessed": "2020-02-10T16:01:15.357-05:00[America/New_York]",
            "path": "G:/SHARE/HuBMAP/Codex_dataset_hubmap/src_CX_19-002_CC2-spleen-A",
            "outputPath": "G:/SHARE/HuBMAP/Codex_dataset_hubmap/src_CX_19-002_CC2-spleen-A",
            "objectiveType": "air",
            "magnification": 20,
            "aperture": 0.75,
            "xyResolution": 377.4463383838384,
            "zPitch": 1500.0,
            "wavelengths": [
                358,
                488,
                550,
                650
            ],
            "bitDepth": 16,
            "numRegions": 1,
            "numCycles": 9,
            "numZPlanes": 13,
            "numChannels": 4,
            "regionWidth": 9,
            "regionHeight": 9,
            "tileWidth": 1920,
            "tileHeight": 1440,
            "tileOverlapX": 0.3,
            "tileOverlapY": 0.3,
            "tilingMode": "snakerows",
            "referenceCycle": 2,
            "referenceChannel": 1,
            "numSubTiles": 1,
            "deconvolutionIterations": 25,
            "deconvolutionModel": "vectorial",
            "focusingOffset": 0,
            "useBackgroundSubtraction": true,
            "useDeconvolution": true,
            "useExtendedDepthOfField": true,
            "useShadingCorrection": true,
            "use3dDriftCompensation": true,
            "useBleachMinimizingCrop": false,
            "useBlindDeconvolution": false,
            "useDiagnosticMode": true,
            "channelNames": {
                "channelNamesArray": [
                    "DAPI-01",
                    "Blank",
                    "Blank",
                    "Blank",
                    "DAPI-02",
                    "CD31",
                    "CD8",
                    "CD45",
                    "DAPI-03",
                    "CD20",
                    "Ki67",
                    "CD3e",
                    "DAPI-04",
                    "Actin",
                    "Podoplan",
                    "CD68",
                    "DAPI-05",
                    "PanCK",
                    "CD21",
                    "CD4",
                    "DAPI-06",
                    "Empty",
                    "CD45RO",
                    "CD11c",
                    "DAPI-07",
                    "Empty",
                    "E-CAD",
                    "CD107a",
                    "DAPI-08",
                    "Empty",
                    "CD44",
                    "H3",
                    "DAPI-09",
                    "Blank",
                    "Blank",
                    "Blank"
                ]
            },
            "exposureTimes": {
                "exposureTimesArray": [
                    [
                        "Cycle",
                        "CH1",
                        "CH2",
                        "CH3",
                        "CH4"
                    ],
                    [
                        "1",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "2",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "3",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "4",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "5",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "6",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "7",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "8",
                        "10",
                        "500",
                        "350",
                        "500"
                    ],
                    [
                        "9",
                        "10",
                        "500",
                        "350",
                        "500"
                    ]
                ]
            },
            "projName": "src_CX_19-002_CC2-spleen-A",
            "regIdx": [
                1
            ],
            "cycle_lower_limit": 1,
            "cycle_upper_limit": 9,
            "num_z_planes": 1,
            "region_width": 9,
            "region_height": 9,
            "tile_width": 1344,
            "tile_height": 1008
        }
    ],
    "required": [
        "version",
        "name",
        "runName",
        "dateProcessed",
        "objectiveType",
        "magnification",
        "aperture",
        "xyResolution",
        "zPitch",
        "wavelengths",
        "bitDepth",
        "numRegions",
        "numCycles",
        "numZPlanes",
        "numChannels",
        "regionWidth",
        "regionHeight",
        "tileWidth",
        "tileHeight",
        "tileOverlapX",
        "tileOverlapY",
        "tilingMode",
        "referenceCycle",
        "referenceChannel",
        "numSubTiles",
        "channelNames",
        "exposureTimes"
    ],
    "properties": {
        "version": {
            "$id": "#/properties/version",
            "type": "string",
            "title": "The version schema",
            "description": "Version of Akoya software",
            "default": "",
            "examples": [
                "1.7.0.6"
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "Experiment name",
            "default": "",
            "examples": [
                "src_CX_19-002_CC2-spleen-A"
            ]
        },
        "runName": {
            "$id": "#/properties/runName",
            "type": "string",
            "title": "The runName schema",
            "description": "Name of run",
            "default": "",
            "examples": [
                "2020-02-10"
            ]
        },
        "dateProcessed": {
            "$id": "#/properties/dateProcessed",
            "type": "string",
            "title": "The dateProcessed schema",
            "description": "Date of processing",
            "default": "",
            "examples": [
                "2020-02-10T16:01:15.357-05:00[America/New_York]"
            ]
        },
        "objectiveType": {
            "$id": "#/properties/objectiveType",
            "type": "string",
            "title": "The objectiveType schema",
            "description": "Objective type",
            "default": "",
            "examples": [
                "air"
            ]
        },
        "magnification": {
            "$id": "#/properties/magnification",
            "type": "integer",
            "title": "The magnification schema",
            "description": "Objective magnification",
            "default": 0,
            "examples": [
                20
            ]
        },
        "aperture": {
            "$id": "#/properties/aperture",
            "type": "number",
            "title": "The aperture schema",
            "description": "Aperture number",
            "default": 0.0,
            "examples": [
                0.75
            ]
        },
        "xyResolution": {
            "$id": "#/properties/xyResolution",
            "type": "number",
            "title": "The xyResolution schema",
            "description": "Lateral resolution",
            "default": 0.0,
            "examples": [
                377.4463383838384
            ]
        },
        "zPitch": {
            "$id": "#/properties/zPitch",
            "type": "number",
            "title": "The zPitch schema",
            "description": "Axial resolution",
            "default": 0.0,
            "examples": [
                1500.0
            ]
        },
        "wavelengths": {
            "$id": "#/properties/wavelengths",
            "type": "array",
            "title": "The wavelengths schema",
            "description": "Emission wavelengths",
            "items": {"type": "integer"},
            "default": [],
            "examples": [
                [
                    358,
                    488
                ]
            ]
        },
        "bitDepth": {
            "$id": "#/properties/bitDepth",
            "type": "integer",
            "title": "The bitDepth schema",
            "description": "Image bit depth",
            "multipleOf": 2,
            "default": 16,
            "examples": [
                16
            ]
        },
        "numRegions": {
            "$id": "#/properties/numRegions",
            "type": "integer",
            "title": "The numRegions schema",
            "description": "Number of regions",
            "minimum": 1,
            "default": 1,
            "examples": [
                1
            ]
        },
        "numCycles": {
            "$id": "#/properties/numCycles",
            "type": "integer",
            "title": "The numCycles schema",
            "description": "Number of cycles",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "numZPlanes": {
            "$id": "#/properties/numZPlanes",
            "type": "integer",
            "title": "The numZPlanes schema",
            "description": "Number of z-planes",
            "minimum": 1,
            "default": 1,
            "examples": [
                13
            ]
        },
        "numChannels": {
            "$id": "#/properties/numChannels",
            "type": "integer",
            "title": "The numChannels schema",
            "description": "Number of channels",
            "minimum": 1,
            "default": 1,
            "examples": [
                4
            ]
        },
        "regionWidth": {
            "$id": "#/properties/regionWidth",
            "type": "integer",
            "title": "The regionWidth schema",
            "description": "Number of tiles in x direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "regionHeight": {
            "$id": "#/properties/regionHeight",
            "type": "integer",
            "title": "The regionHeight schema",
            "description": "Number of tiles in y direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "tileWidth": {
            "$id": "#/properties/tileWidth",
            "type": "integer",
            "title": "The tileWidth schema",
            "description": "Tile width with overlap",
            "default": 1,
            "examples": [
                1920
            ]
        },
        "tileHeight": {
            "$id": "#/properties/tileHeight",
            "type": "integer",
            "title": "The tileHeight schema",
            "description": "Tile height with overlap",
            "default": 1,
            "examples": [
                1440
            ]
        },
        "tileOverlapX": {
            "$id": "#/properties/tileOverlapX",
            "type": "number",
            "title": "The tileOverlapX schema",
            "description": "Horizontal overlap between adjacent tiles in fractions of 1",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "tileOverlapY": {
            "$id": "#/properties/tileOverlapY",
            "type": "number",
            "title": "The tileOverlapY schema",
            "description": "Vertical overlap between adjacent tiles in fractions of 1",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "tilingMode": {
            "$id": "#/properties/tilingMode",
            "type": "string",
            "title": "The tilingMode schema",
            "description": "Tiling mode snake, grid, maybe something else",
            "default": "",
            "examples": [
                "snakerows"
            ]
        },
        "referenceCycle": {
            "$id": "#/properties/referenceCycle",
            "type": "integer",
            "title": "The referenceCycle schema",
            "description": "Cycle with reference channel",
            "default": 1,
            "minimum": 1,
            "examples": [
                2
            ]
        },
        "referenceChannel": {
            "$id": "#/properties/referenceChannel",
            "type": "integer",
            "title": "The referenceChannel schema",
            "description": "Channel to be used as a reference for processing and segmentation",
            "default": 1,
            "minimum": 1,
            "examples": [
                1
            ]
        },
        "numSubTiles": {
            "$id": "#/properties/numSubTiles",
            "type": "integer",
            "title": "The numSubTiles schema",
            "description": "Not sure what subtile is, should be 1",
            "default": 1,
            "maximum": 1,
            "examples": [
                1
            ]
        },
        "channelNames": {
            "$id": "#/properties/channelNames",
            "type": "object",
            "title": "The channelNames schema",
            "description": "List of names across cycles",
            "default": {},
            "examples": [
                {
                    "channelNamesArray": [
                        "DAPI-01",
                        "Blank",
                        "Blank",
                        "Blank",
                        "DAPI-02",
                        "CD31",
                        "CD8",
                        "CD45"
                    ]
                }
            ],
            "required": [
                "channelNamesArray"
            ],
            "properties": {
                "channelNamesArray": {
                    "$id": "#/properties/channelNames/properties/channelNamesArray",
                    "type": "array",
                    "title": "The channelNamesArray schema",
                    "description": "An explanation about the purpose of this instance.",
                    "items": {"type": "string", "pattern": "^[A-Za-z0-9_. /-]*$"},
                    "default": [],
                    "examples": [
                        [
                            "DAPI-01",
                            "Blank"
                        ]
                    ]
                  }
                }
        },
        "exposureTimes": {
            "$id": "#/properties/exposureTimes",
            "type": "object",
            "title": "The exposureTimes schema",
            "description": "An explanation about the purpose of this instance.",
            "default": {},
            "examples": [
                {
                    "exposureTimesArray": [
                        [
                            "Cycle",
                            "CH1",
                            "CH2",
                            "CH3",
                            "CH4"
                        ],
                        [
                            "1",
                            "10",
                            "500",
                            "350",
                            "500"
                        ],
                        [
                            "2",
                            "10",
                            "500",
                            "350",
                            "500"
                        ]
                    ]
                }
            ],
            "required": [
                "exposureTimesArray"
            ],
            "properties": {
                "exposureTimesArray": {
                    "$id": "#/properties/exposureTimes/properties/exposureTimesArray",
                    "type": "array",
                    "title": "The exposureTimesArray schema",
                    "description": "List of exposure times for each cycle and channel",
                    "minItems": 2,
                    "default": [],
                    "examples": [
                        [
                            [
                                "Cycle",
                                "CH1",
                                "CH2",
                                "CH3",
                                "CH4"
                            ],
                            [
                                "1",
                                "10",
                                "500",
                                "350",
                                "500"
                            ]
                        ]
                    ],
                    "items": {
                        "$id": "#/properties/exposureTimes/properties/exposureTimesArray/items",
                        "anyOf": [
                            {
                                "$id": "#/properties/exposureTimes/properties/exposureTimesArray/items/anyOf/0",
                                "type": "array",
                                "title": "The first anyOf schema",
                                "description": "Names of fields",
                                "items":{"type": "string"},
                                "default": [],
                                "examples": [
                                    [
                                        "Cycle",
                                        "CH1"
                                    ]
                                ]
                            },
                            {
                                "$id": "#/properties/exposureTimes/properties/exposureTimesArray/items/anyOf/1",
                                "type": "array",
                                "title": "The second anyOf schema",
                                "description": "Cycle id and exposure time",
                                "items":{"type": "string"},
                                "default": [],
                                "examples": [
                                    [
                                        "1",
                                        "750"
                                    ]
                                ]
                            }
                        ]
                    }
                }
            }
        },
        "projName": {
            "$id": "#/properties/projName",
            "type": "string",
            "title": "The projName schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "src_CX_19-002_CC2-spleen-A"
            ]
        },
        "regIdx": {
            "$id": "#/properties/regIdx",
            "type": "array",
            "title": "The regIdx schema",
            "description": "Region ids",
            "items": {"type": "integer"},
            "uniqueItems": true,
            "minimum": 1,
            "default": [1],
            "examples": [
                [
                    1,2,3
                ]
            ]
        },
        "cycle_lower_limit": {
            "$id": "#/properties/cycle_lower_limit",
            "type": "integer",
            "title": "The cycle_lower_limit schema",
            "description": "First cycle id in the dataset",
            "minimum":1,
            "default": 1,
            "examples": [
                1
            ]
        },
        "cycle_upper_limit": {
            "$id": "#/properties/cycle_upper_limit",
            "type": "integer",
            "title": "The cycle_upper_limit schema",
            "description": "Maximum cycle id the dataset",
            "minimum":1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "num_z_planes": {
            "$id": "#/properties/num_z_planes",
            "type": "integer",
            "title": "The num_z_planes schema",
            "description": "Number of z-planes",
            "minimum": 1,
            "default": 1,
            "examples": [
                1
            ]
        },
        "region_width": {
            "$id": "#/properties/region_width",
            "type": "integer",
            "title": "The region_width schema",
            "description": "Number of tiles in x direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "region_height": {
            "$id": "#/properties/region_height",
            "type": "integer",
            "title": "The region_height schema",
            "description": "Number of tiles in y direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "tile_width": {
            "$id": "#/properties/tile_width",
            "type": "integer",
            "title": "The tile_width schema",
            "description": "Tile width without overlap",
            "minimum": 1,
            "default": 1,
            "examples": [
                1344
            ]
        },
        "tile_height": {
            "$id": "#/properties/tile_height",
            "type": "integer",
            "title": "The tile_height schema",
            "description": "Tile height without overlap",
            "minimum": 1,
            "default": 1,
            "examples": [
                1008
            ]
        }
    },
    "additionalProperties": true
}
"""

_experiment_1_5_schema_str = """{
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
          "version": "1.5.0.38",
          "name": "19-001_SP_CC2-A_03232021",
          "dateProcessed": "2021-03-24T08:51:26.7853506-04:00",
          "path": "F:/RUNS_1",
          "outputPath": "",
          "objectiveType": "air",
          "magnification": 20,
          "aperture": 0.75,
          "xyResolution": 377.44633838383839,
          "zPitch": 1500.0,
          "wavelengths": [
            358,
            488,
            550,
            650
          ],
          "bitness": 16,
          "numRegions": 1,
          "numCycles": 13,
          "numTiles": 63,
          "numZPlanes": 19,
          "numChannels": 4,
          "regionWidth": 9,
          "regionHeight": 7,
          "tileWidth": 1920,
          "tileHeight": 1440,
          "tileOverlapX": 0.3,
          "tileOverlapY": 0.3,
          "tilingMode": "snakeRows",
          "backgroundSubtractionMode": "min-min",
          "deconvolution": "Microvolution",
          "driftCompReferenceCycle": 2,
          "driftCompReferenceChannel": 1,
          "bestFocusReferenceCycle": 2,
          "bestFocusReferenceChannel": 1,
          "numSubTiles": 1,
          "focusingOffset": 0,
          "useFlatFieldCorrection": true,
          "useBackgroundSubtraction": true,
          "HandEstain": false,
          "use3dDriftCompensation": true,
          "useBleachMinimizingCrop": false,
          "useBlindDeconvolution": false,
          "useDiagnosticMode": false,
          "useShadingCorrection": true
        }
    ],
    "required": [
        "version",
        "name",
        "dateProcessed",
        "objectiveType",
        "magnification",
        "aperture",
        "xyResolution",
        "zPitch",
        "wavelengths",
        "bitness",
        "numRegions",
        "numCycles",
        "numZPlanes",
        "numChannels",
        "regionWidth",
        "regionHeight",
        "tileWidth",
        "tileHeight",
        "tileOverlapX",
        "tileOverlapY",
        "tilingMode",
        "driftCompReferenceCycle",
        "driftCompReferenceChannel",
        "bestFocusReferenceCycle",
        "bestFocusReferenceChannel",
        "numSubTiles"
    ],
    "properties": {
        "version": {
            "$id": "#/properties/version",
            "type": "string",
            "title": "The version schema",
            "description": "Version of Akoya software",
            "default": "",
            "examples": [
                "1.5.0.38"
            ]
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "Experiment name",
            "default": "",
            "examples": [
                "src_CX_19-002_CC2-spleen-A"
            ]
        },
        "dateProcessed": {
            "$id": "#/properties/dateProcessed",
            "type": "string",
            "title": "The dateProcessed schema",
            "description": "Date of processing",
            "default": "",
            "examples": [
                "2020-02-10T16:01:15.357-05:00[America/New_York]"
            ]
        },
        "objectiveType": {
            "$id": "#/properties/objectiveType",
            "type": "string",
            "title": "The objectiveType schema",
            "description": "Objective type",
            "default": "",
            "examples": [
                "air"
            ]
        },
        "magnification": {
            "$id": "#/properties/magnification",
            "type": "integer",
            "title": "The magnification schema",
            "description": "Objective magnification",
            "default": 0,
            "examples": [
                20
            ]
        },
        "aperture": {
            "$id": "#/properties/aperture",
            "type": "number",
            "title": "The aperture schema",
            "description": "Aperture number",
            "default": 0.0,
            "examples": [
                0.75
            ]
        },
        "xyResolution": {
            "$id": "#/properties/xyResolution",
            "type": "number",
            "title": "The xyResolution schema",
            "description": "Lateral resolution",
            "default": 0.0,
            "examples": [
                377.4463383838384
            ]
        },
        "zPitch": {
            "$id": "#/properties/zPitch",
            "type": "number",
            "title": "The zPitch schema",
            "description": "Axial resolution",
            "default": 0.0,
            "examples": [
                1500.0
            ]
        },
        "wavelengths": {
            "$id": "#/properties/wavelengths",
            "type": "array",
            "title": "The wavelengths schema",
            "description": "Emission wavelengths",
            "items": {
                "type": "integer"
            },
            "default": [],
            "examples": [
                [
                    358,
                    488
                ]
            ]
        },
        "bitness": {
            "$id": "#/properties/bitness",
            "type": "integer",
            "title": "The bitness schema",
            "description": "Image bit depth",
            "multipleOf": 2,
            "default": 16,
            "examples": [
                16
            ]
        },
        "numRegions": {
            "$id": "#/properties/numRegions",
            "type": "integer",
            "title": "The numRegions schema",
            "description": "Number of regions",
            "minimum": 1,
            "default": 1,
            "examples": [
                1
            ]
        },
        "numCycles": {
            "$id": "#/properties/numCycles",
            "type": "integer",
            "title": "The numCycles schema",
            "description": "Number of cycles",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "numZPlanes": {
            "$id": "#/properties/numZPlanes",
            "type": "integer",
            "title": "The numZPlanes schema",
            "description": "Number of z-planes",
            "minimum": 1,
            "default": 1,
            "examples": [
                13
            ]
        },
        "numChannels": {
            "$id": "#/properties/numChannels",
            "type": "integer",
            "title": "The numChannels schema",
            "description": "Number of channels",
            "minimum": 1,
            "default": 1,
            "examples": [
                4
            ]
        },
        "regionWidth": {
            "$id": "#/properties/regionWidth",
            "type": "integer",
            "title": "The regionWidth schema",
            "description": "Number of tiles in x direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "regionHeight": {
            "$id": "#/properties/regionHeight",
            "type": "integer",
            "title": "The regionHeight schema",
            "description": "Number of tiles in y direction",
            "minimum": 1,
            "default": 1,
            "examples": [
                9
            ]
        },
        "tileWidth": {
            "$id": "#/properties/tileWidth",
            "type": "integer",
            "title": "The tileWidth schema",
            "description": "Tile width with overlap",
            "default": 1,
            "examples": [
                1920
            ]
        },
        "tileHeight": {
            "$id": "#/properties/tileHeight",
            "type": "integer",
            "title": "The tileHeight schema",
            "description": "Tile height with overlap",
            "default": 1,
            "examples": [
                1440
            ]
        },
        "tileOverlapX": {
            "$id": "#/properties/tileOverlapX",
            "type": "number",
            "title": "The tileOverlapX schema",
            "description": "Horizontal overlap between adjacent tiles in fractions of 1",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "tileOverlapY": {
            "$id": "#/properties/tileOverlapY",
            "type": "number",
            "title": "The tileOverlapY schema",
            "description": "Vertical overlap between adjacent tiles in fractions of 1",
            "default": 0.0,
            "examples": [
                0.3
            ]
        },
        "tilingMode": {
            "$id": "#/properties/tilingMode",
            "type": "string",
            "title": "The tilingMode schema",
            "description": "Tiling mode snake, grid, maybe something else",
            "default": "",
            "examples": [
                "snakerows"
            ]
        },
        "bestFocusReferenceCycle": {
            "$id": "#/properties/bestFocusReferenceCycle",
            "type": "integer",
            "title": "The bestFocusReferenceCycle schema",
            "description": "Cycle with reference channel",
            "default": 1,
            "minimum": 1,
            "examples": [
                2
            ]
        },
        "bestFocusReferenceChannel": {
            "$id": "#/properties/referenceChannel",
            "type": "integer",
            "title": "The bestFocusReferenceChannel schema",
            "description": "Channel to be used as a reference for processing and segmentation",
            "default": 1,
            "minimum": 1,
            "examples": [
                1
            ]
        },
        "driftCompReferenceCycle": {
            "$id": "#/properties/driftCompReferenceCycle",
            "type": "integer",
            "title": "The driftCompReferenceCycle schema",
            "description": "Cycle with reference channel",
            "default": 1,
            "minimum": 1,
            "examples": [
                2
            ]
        },
        "driftCompReferenceChannel": {
            "$id": "#/properties/driftCompReferenceChannel",
            "type": "integer",
            "title": "The bestFocusReferenceChannel schema",
            "description": "Channel to be used as a reference for image registration",
            "default": 1,
            "minimum": 1,
            "examples": [
                1
            ]
        },
        "deconvolutionIterations": {
            "$id": "#/properties/deconvolutionIterations",
            "type": "integer",
            "title": "The deconvolutionIterations schema",
            "description": "TMC - Number of deconvolution iterations",
            "default": 0,
            "examples": [
                25
            ]
        },
        "deconvolutionModel": {
            "$id": "#/properties/deconvolutionModel",
            "type": "string",
            "title": "The deconvolutionModel schema",
            "description": "TMC - Deconvolution model",
            "default": "",
            "examples": [
                "vectorial"
            ]
        },
        "focusingOffset": {
            "$id": "#/properties/focusingOffset",
            "type": "integer",
            "title": "The focusingOffset schema",
            "description": "TMC - I have no idea what it is, usually 0",
            "default": 0,
            "examples": [
                0
            ]
        }
    },
    "numSubTiles": {
        "$id": "#/properties/numSubTiles",
        "type": "integer",
        "title": "The numSubTiles schema",
        "description": "Not sure what subtile is, should be 1",
        "default": 1,
        "maximum": 1,
        "examples": [
            1
        ]
    },
    "additionalProperties": true
}
"""


dataset_schema = json.loads(_dataset_schema_str)
experiment_1_7_schema = json.loads(_experiment_1_7_schema_str)
experiment_1_5_schema = json.loads(_experiment_1_5_schema_str)


def get_experiment_metadata_schema(metadata: dict):
    ver = metadata.get("version", None)
    if ver is None:
        msg = "Could not find field version in the experiment.json metadata"
        raise ValueError(msg)
    if version.parse(ver) >= version.parse("1.7") < version.parse("1.8"):
        return experiment_1_7_schema
    elif version.parse(ver) >= version.parse("1.5") < version.parse("1.7"):
        return experiment_1_5_schema
    else:
        msg = (
            f"The version {str(ver)} of experiment.json is not supported."
            + "Supported version are 1.5 and 1.7"
        )
        raise NotImplementedError(msg)
