import os
import sys
import pytest
from dynamic_argument_parser import DynamicArgumentParser
from config import ExperimentConfig


def test_parser_can_parse_from_json():
    cli_args = [
        "--config_values",
        "sample/values.json",
    ]
    parser = DynamicArgumentParser()
    args = parser.parse_args(cli_args)
    assert args.boolean_parameter_1 == True
    assert args.float_parameter_1 == 1
    assert args.list_parameter_1 == [0]
    assert args.str_parameter_1 == "None"


@pytest.mark.skip(reason="Test is not implemented")
def test_parser_can_parse_from_json_using_a_different_config_schema():
    # TODO: impl
    pass


def test_parser_can_create_a_nested_config():
    cli_args = [
        "--config_schema",
        "nested",
        "--config_values",
        "sample/nested_config_values.json",
    ]
    parser = DynamicArgumentParser()
    args = parser.parse_args(cli_args)
    config = ExperimentConfig.from_args(args)
    # print(config)
    # print(ExperimentConfig.__pydantic_model__.schema())
    # assert False
    assert config.training.data.paths == ["data/00*.csv", "data/01*.csv"]
    assert config.model.type == "boosted_tree"
    assert config.model.parameters["learning_rate"] == 0.01


@pytest.mark.skip(reason="Test is not implemented")
def test_parser_can_create_a_nested_config_and_override_its_values_using_args():
    # TODO: impl
    pass


def test_parser_prints_out_example_nested_config():
    help_msg = DynamicArgumentParser().format_help()
    assert "An example config file:" in help_msg


# TODO: add tests for randomly generated parameters.
# TODO: add tests to immitate how the nested experiment config
#   is intened to be used in a new project, to easily subclass and compose various nested configs.


def test_experiment_config_can_be_customized_in_a_new_project():
    from pydantic.dataclasses import dataclass
    from dataclasses import field

    # Inheriting ExperimentConfig does not work, without adding @dataclass!
    @dataclass
    class SiameseExperimentConfig(ExperimentConfig):
        """A training pipeline for training siamese models."""

        @dataclass
        class LossConfig:
            mse_loss_weight: float = 0.1
            log_loss_weight: float = 0.5

        loss: LossConfig = field(default_factory=LossConfig)

    config_dict = {"loss": {"mse_loss_weight": 0.2}, "model": {}}
    c = SiameseExperimentConfig(**config_dict)
    assert c.loss.mse_loss_weight == 0.2
    assert c.model.type == "boosted_tree"
