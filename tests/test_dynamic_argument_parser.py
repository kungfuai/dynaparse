import os
import sys
from dynamic_argument_parser import DynamicArgumentParser


def test_parser_can_parse_from_json():
    argv_called = sys.argv
    try:
        sys.argv = [
            "test_command",
            "--config_schema",
            "sample/schema.json",
            "--config_values",
            "sample/values.json",
        ]
        parser = DynamicArgumentParser()
        args = parser.parse_args()
        assert args.boolean_parameter_1 == True
        assert args.float_parameter_1 == 1
        assert args.list_parameter_1 == [0]
    except Exception as e:
        raise Exception(e)
    finally:
        sys.argv = argv_called
