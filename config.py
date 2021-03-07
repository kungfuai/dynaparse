from typing import List, Dict
from dataclasses_json import dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin
from argparse import Namespace
import dataclasses as dc
from pydantic.dataclasses import dataclass
import os
import json

from parameters.int_parameter import IntParameter
from parameters.float_parameter import FloatParameter


@dataclass
class ModelConfig:
    type: str = "boosted_tree"
    parameters: Dict = dc.field(default_factory=dict)


@dataclass
class DataConfig:
    @dataclass
    class AugmentationConfig:
        method: str = None
        kwargs: Dict = dc.field(default_factory=lambda _: {})
        column: str = None  # For tabular data only.

    paths: List[str] = None
    augmentation: List[AugmentationConfig] = None


@dataclass
class TrainingConfig:
    data: DataConfig = None
    epochs: int = dc.field(
        # TODO: implement __repr__ or __str__ of the sample() method to display
        #   useful help information, including low, high, distribution.
        default_factory=IntParameter(
            default=10,
            low=5,
            high=100,
            distribution="uniform",
            name="",
            help="",
            required=True,
        ).sample
    )
    learning_rate: float = dc.field(
        default_factory=FloatParameter(
            default=0.001,
            low=1e-6,
            high=0.01,
            distribution="uniform",
            name="",
            help="",
            required=True,
        ).sample
    )


@dataclass
class EvaluationConfig:
    data: DataConfig = None


@dataclass
class ExperimentConfig:
    model: ModelConfig
    training: TrainingConfig = None
    evaluation: EvaluationConfig = None

    @classmethod
    def from_args(cls, args: Namespace):
        config_file_path = args.config_values
        return cls.from_file(config_file_path)

    @classmethod
    def from_file(cls, config_file_path):
        if not os.path.isfile(config_file_path):
            raise IOError(f"Config file not found: {config_file_path}")
        config_dict = json.load(open(config_file_path))
        return cls(**config_dict)


if __name__ == "__main__":
    from jsonargparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_class_arguments(Config)
    args = parser.parse_args()