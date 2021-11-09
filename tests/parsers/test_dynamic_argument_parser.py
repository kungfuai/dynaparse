from argparse import ArgumentDefaultsHelpFormatter
import pytest
import unittest
import sys

from dynaparse import DynamicArgumentParser
from tests.data.config_class_example import ConfigClassExample

SYS_ARGV = sys.argv


def get_sample_parser(*args, **kwargs):
    class SampleParser(DynamicArgumentParser):
        def __init__(self):
            super().__init__(
                prog="test_script",
                description="Test description",
                formatter_class=ArgumentDefaultsHelpFormatter,
            )
            if len(args) > 0 and len(kwargs) > 0:
                self.add_argument(*args, **kwargs)

    return SampleParser


class TestDynamicArgumentParser(unittest.TestCase):
    def tearDown(self):
        sys.argv = SYS_ARGV

    def test_init_when_valid(self):
        sys.argv = []
        tp = get_sample_parser()()
        assert tp.prog == "test_script"
        assert tp.usage is None
        assert tp.description == "Test description"
        assert tp.formatter_class == ArgumentDefaultsHelpFormatter
        assert tp.conflict_handler == "error"
        assert tp.add_help is True

    def test_parse_args_when_spec_only(self):
        sys.argv = ["script.sh", "--spec", "tests/data/spec_example.json"]
        tp = get_sample_parser()()
        args = tp.parse_args()
        assert args.boolean_parameter_1 is True
        assert args.categorical_parameter_1 == "option1"
        assert args.config is None
        assert args.float_parameter_1 == 1.0
        assert args.list_parameter_1 == [0, 1, 2]
        assert args.nested_section.int_parameter_1 == 1
        assert args.nested_section.str_parameter_1 is None
        assert args.random_sample is False
        assert args.spec == "tests/data/spec_example.json"

    def test_parse_args_when_config_override_json(self):
        sys.argv = [
            "script.sh",
            "--spec",
            "tests/data/spec_example.json",
            "--config",
            "tests/data/config_example.json",
        ]
        tp = get_sample_parser()()
        args = tp.parse_args()
        assert args.boolean_parameter_1 is False
        assert args.categorical_parameter_1 == "option2"
        assert args.config is "tests/data/config_example.json"
        assert args.float_parameter_1 == 2.0
        assert args.list_parameter_1 == [2, 1, 0]
        assert args.nested_section.int_parameter_1 == 2
        assert args.nested_section.str_parameter_1 == "test"
        assert args.random_sample is False
        assert args.spec == "tests/data/spec_example.json"

    def test_parse_args_when_config_override_yaml(self):
        sys.argv = [
            "script.sh",
            "--spec",
            "tests/data/spec_example.json",
            "--config",
            "tests/data/config_example.yaml",
        ]
        tp = get_sample_parser()()
        args = tp.parse_args()
        assert args.boolean_parameter_1 is False
        assert args.categorical_parameter_1 == "option2"
        assert args.config is "tests/data/config_example.yaml"
        assert args.float_parameter_1 == 2.0
        assert args.list_parameter_1 == [2, 1, 0]
        assert args.nested_section.int_parameter_1 == 2
        assert args.nested_section.str_parameter_1 == "test"
        assert args.random_sample is False
        assert args.spec == "tests/data/spec_example.json"

    def test_parse_args_when_cmdline_override_class_config(self):
        """
        When the parser is appended a class-based config object,
        it should add arugments for the nested fields, so that a command like:
            "script.sh --optimizer.lr 0.1"
        can be used override a nested config object:
            config_object.optimizer.lr = 0.1
        """
        sys.argv = ["script.sh", "--component.height", "5"]
        config_obj = ConfigClassExample()
        parser = DynamicArgumentParser()
        parser.append_config(config_obj)
        args = parser.parse_args()
        assert "--component.component1.size" in parser.format_help()
        assert args.component.component1.size == config_obj.component.component1.size
        assert args.component.height == 5

    def test_parse_args_when_cmdline_override(self):
        sys.argv = [
            "script.sh",
            "--spec",
            "tests/data/spec_example.json",
            "--boolean_parameter_1",
            "true",
            "--categorical_parameter_1",
            "option3",
            "--config",
            "tests/data/config_example.json",
            "--float_parameter_1",
            "5.0",
            "--list_parameter_1",
            "5",
            "6",
            "7",
            "--nested_section.int_parameter_1",
            "5",
            "--nested_section.str_parameter_1",
            "test2",
        ]
        tp = get_sample_parser()()
        args = tp.parse_args()
        assert args.boolean_parameter_1 is True
        assert args.categorical_parameter_1 == "option3"
        assert args.config == "tests/data/config_example.json"
        assert args.float_parameter_1 == 5.0
        assert args.list_parameter_1 == [5, 6, 7]
        assert args.nested_section.int_parameter_1 == 5
        assert args.nested_section.str_parameter_1 == "test2"
        assert args.random_sample is False
        assert args.spec == "tests/data/spec_example.json"

    def test_when_spec_argname_conflict(self):
        Parser = get_sample_parser("--spec", type=int, default=None)
        with pytest.raises(Exception):
            Parser()

    def test_when_config_argname_conflict(self):
        Parser = get_sample_parser("--config", type=int, default=None)
        with pytest.raises(Exception):
            Parser()

    def test_when_random_sample_argname_conflict(self):
        Parser = get_sample_parser("--random_sample", type=int, default=None)
        with pytest.raises(Exception):
            Parser()
