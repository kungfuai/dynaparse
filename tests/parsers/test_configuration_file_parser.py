import json
from unittest.mock import patch

from dynaparse.parsers.configuration_file_parser import ConfigurationFileParser

with open("tests/data/config_example.json", "r") as fd:
    raw_config = json.load(fd)
with open("tests/data/spec_example.json", "r") as fd:
    raw_spec = json.load(fd)


def test_load_flat_spec():
    with patch(
        "dynaparse.parsers.configuration_file_parser.ConfigurationFileParser._flatten_nested_structure"
    ) as patched_flatten:
        patched_flatten.return_value = "test"
        parsed = ConfigurationFileParser.load_flat_spec("tests/data/spec_example.json")
        assert parsed == "test"
        assert patched_flatten.called_with(raw_spec)


def test_load_flat_config_when_json():
    with patch(
        "dynaparse.parsers.configuration_file_parser.ConfigurationFileParser._flatten_nested_structure"
    ) as patched_flatten:
        patched_flatten.return_value = "test"
        parsed = ConfigurationFileParser.load_flat_config(
            "tests/data/config_example.json"
        )
        assert parsed == "test"
        assert patched_flatten.called_with(raw_config)


def test_load_flat_config_when_yaml():
    with patch(
        "dynaparse.parsers.configuration_file_parser.ConfigurationFileParser._flatten_nested_structure"
    ) as patched_flatten:
        patched_flatten.return_value = "test"
        parsed = ConfigurationFileParser.load_flat_config(
            "tests/data/config_example.yaml"
        )
        assert parsed == "test"
        assert patched_flatten.called_with(raw_config)


def test_expand_flat_spec():
    with patch(
        "dynaparse.parsers.configuration_file_parser.ConfigurationFileParser._expand_flat_structure"
    ) as patched_expand:
        patched_expand.return_value = "test"
        ans = ConfigurationFileParser.expand_flat_spec("test_spec")
        assert ans == "test"
        assert patched_expand.called_with({"structure": "test_spec", "is_spec": True})


def test_expand_flat_config():
    with patch(
        "dynaparse.parsers.configuration_file_parser.ConfigurationFileParser._expand_flat_structure"
    ) as patched_expand:
        patched_expand.return_value = "test"
        ans = ConfigurationFileParser.expand_flat_config("test_config")
        assert ans == "test"
        assert patched_expand.called_with(
            {"structure": "test_config", "is_spec": False}
        )


def test_is_parameter_dict_when_true():
    test_dict = {
        "name": "test_name",
        "help": "test_help",
        "required": True,
        "default": "test",
    }
    assert ConfigurationFileParser._is_parameter_dict(test_dict) is True


def test_is_parameter_dict_when_not_true():
    test_dict = {
        "testname": "test_name",
        "testhelp": "test_help",
        "testrequired": True,
        "testdefault": "test",
    }
    assert ConfigurationFileParser._is_parameter_dict(test_dict) is False


def test_get_parameter_type_when_param_dict():
    test_dict = {
        "name": "test_name",
        "help": "test_help",
        "required": True,
        "default": "test",
    }
    assert ConfigurationFileParser._get_parameter_type(test_dict) == "parameter_dict"


def test_get_parameter_type_when_nonparam_dict():
    test_dict = {
        "testname": "test_name",
        "testhelp": "test_help",
        "testrequired": True,
        "testdefault": "test",
    }
    assert ConfigurationFileParser._get_parameter_type(test_dict) == "parent"


def test_get_parameter_type_when_param_list():
    test_list = [0, 1, 2]
    assert ConfigurationFileParser._get_parameter_type(test_list) == "parameter_value"


def test_get_parameter_type_when_param_value():
    test_value = 0
    assert ConfigurationFileParser._get_parameter_type(test_value) == "parameter_value"
