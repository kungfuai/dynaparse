from dataclasses import dataclass
from typing import List, Dict
from dataclasses_json import dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin
from dataclasses import dataclass, is_dataclass
from argparse import Namespace
from dataclass_nested import dataclass_nested
import os
import json


@dataclass_json
@dataclass
class Config(JsonSchemaMixin):
    """testing"""

    train_split_proportion: float
    conv_activation: str
    conv_padding: str
    dense_inter_size: int
    max_pool_filter_size: int
    in_shape: List[int]
    max_num_signatures_per_grab: int
    grab_label_file: str
    length: int
    signal_prop: float
    signal_nonconflation_prop: float
    val_signal_nonconflation_prop: float
    kernel_sizes: List[int]
    filter_sizes: List[int]
    network: str = "test"


@dataclass
class ModelConfig:
    type: str
    parameters: Dict


@dataclass_nested
class DataConfig:
    @dataclass
    class AugmentationConfig:
        method: str
        kwargs: Dict
        column: str = None  # For tabular data only.

    paths: List[str] = None
    augmentation: List[AugmentationConfig] = None


@dataclass_nested
class TrainingConfig:
    data: DataConfig = None
    epochs: int = 10
    learning_rate: float = 1e-3


@dataclass_nested
class EvaluationConfig:
    data: DataConfig = None


# @dataclass_json
@dataclass_nested
class ExperimentConfig:
    model: ModelConfig
    training: TrainingConfig
    evaluation: EvaluationConfig

    @classmethod
    def from_args(cls, args: Namespace):
        config_file_path = args.config_values
        if not os.path.isfile(config_file_path):
            raise IOError(f"Config file not found: {config_file_path}")
        config_dict = json.load(open(config_file_path))
        return cls(**config_dict)


if __name__ == "__main__":
    from jsonargparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_class_arguments(Config)
    args = parser.parse_args()