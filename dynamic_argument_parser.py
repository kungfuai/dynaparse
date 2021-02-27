from argparse import ArgumentParser
import sys
import os
import json

from dynamic_configuration import DynamicConfiguration
from config import ExperimentConfig


class DynamicArgumentParser(ArgumentParser):
    """Extends 'ArgumentParser' to include dynamic functionality."""

    _RESERVED_ARGS = ["config_schema", "config_values", "randomize_config"]

    def __init__(self, schema_class=ExperimentConfig, *args, **kwargs):
        """Initialize new arg parser with dynamic args taken into account."""
        super().__init__(*args, **kwargs)

        self._dynamic_config = DynamicConfiguration()
        self._schema_class = schema_class
        # self._schema_file = self._get_command_line_value_from_arg("config_schema")
        # self._values_file = self._get_command_line_value_from_arg("config_values")

        if self._argument_conflicts_exist():
            raise Exception(
                "The following arguments are reserved for the DynamicArgumentParser: %s"
                % (self._RESERVED_ARGS)
            )

        self.add_argument(
            "--config_values",
            "--config",
            type=str,
            default=None,
            help="File specifying values following the schema in 'config_schema'. These will override command line args if specified.",
        )
        self.add_argument(
            "--randomize_config",
            action="store_true",
            default=False,
            help="If True, generate random parameters from the specified dynamic configuration.",
        )
        self.add_argument(
            "--config_schema",
            type=str,
            default="sample/schema.json",
            help=(
                "Dynamic configuration schema file specifying variable named arguments. "
                "It can be a path to a json file, or a string value 'nested'. If it is 'nested', "
                f"then {self._schema_class} is used to define the schema."
            ),
        )

    def _get_command_line_value_from_arg(self, arg):
        """Return command line value from a specific argument name."""
        arg_str = "--" + arg
        for i in range(len(sys.argv)):
            if sys.argv[i] == arg_str:
                return sys.argv[i + 1]
        return None

    def _check_for_dynamic_config(self, args):
        """Append arguments for a dynamic configuration."""
        if args.config_schema is not None:
            if args.config_schema == "nested":
                pass
            else:
                assert os.path.isfile(args.config_schema), "Schema file not found"
                self._dynamic_config.load_schema(args.config_schema)
                self._dynamic_config.append_to_arg_parser(self)

    def _get_existing_arg_names(self):
        """Get names of arguments loaded as actions."""
        return [a.dest for a in self._actions]

    def _argument_conflicts_exist(self):
        """Check that no arguments were supplied that conflict with reserved ones."""
        existing = set(self._get_existing_arg_names())
        reserved = set(self._RESERVED_ARGS)
        return len(existing.intersection(reserved)) > 0

    def format_help(self):
        """Format help as usual, but append note about dynamic argument parser."""
        help_str = super().format_help()
        help_str += "\n*****\n"
        help_str += f"\nSchema defined by {self._schema_class}:\n"
        help_str += (
            f"{json.dumps(self._schema_class.__pydantic_model__.schema(), indent=2)}"
        )
        help_str += "\n*****\n\nAn example config file:"
        help_str += """
        {
            "model": {
                "type": "boosted_tree",
                "parameters": {
                    "max_depth": 5,
                    "max_leaves": 31,
                    "bagging_fraction": 0.5,
                    "eta": 0.03,
                    "learning_rate": 0.01
                }
            },
            "training": {
                "data": {
                    "paths": [
                        "data/00*.csv",
                        "data/01*.csv"
                    ],
                    "augmentation": [
                        {
                            "method": "fillna",
                            "column": "x",
                            "kwargs": {
                                "value": -1
                            }
                        }
                    ]
                }
            },
            "evaluation": {
                "data": {
                    "paths": [
                        "data/05*.csv"
                    ]
                }
            }
        }
        """
        help_str += "\nNOTE: This script uses a dynamic argument parser for configuration.\nSee ..... for more information.\n"
        return help_str

    def parse_args(self, *largs, **kwargs):
        """Parse all arguments including dynamic configuration-based ones."""
        args = super().parse_args(*largs, **kwargs)
        self._check_for_dynamic_config(args)
        if not self._dynamic_config.has_schema():
            return args

        if args.config_values is not None:
            if args.config_schema is None:
                raise Exception("Can't specify config values without specifying schema")
            self._dynamic_config.load_values(args.config_values)

        self._dynamic_config.patch_sys_argv()

        if self._dynamic_config.has_schema() and args.randomize_config:
            self._dynamic_config.overwrite_args_with_random(args)

        if args.config_values is not None:
            self._dynamic_config.overwrite_args_with_contents(args)

        return args
