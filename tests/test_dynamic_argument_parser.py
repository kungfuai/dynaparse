import os
from dynamic_argument_parser import DynamicArgumentParser


def test_parser_can_parse_from_json():
    parser = DynamicArgumentParser()
    cli_args = ["--config_values", os.path.join("sample", "values.json")]
    args = parser.parse_args(cli_args)
    # assert args == 0
    print(args)
    assert args.boolean_parameter_1 == True
    assert args.float_parameter_1 == 1
    assert args.list_parameter_1 == [0]
