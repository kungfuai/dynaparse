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