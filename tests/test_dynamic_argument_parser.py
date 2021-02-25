import os
import sys
import pytest
from dynamic_argument_parser import DynamicArgumentParser


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


@pytest.mark.skip(reason="Not implemented")
def test_parser_can_parse_a_nested_config():
    cli_args = [
        "--config_schema",
        "nested",
        "--config_values",
        "sample/values.json",
    ]
    parser = DynamicArgumentParser()
    args = parser.parse_args(cli_args)
    assert args.config.train.data.paths == ["data/01*.csv", "data/02*.csv"]