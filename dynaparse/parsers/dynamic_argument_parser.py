import argparse
from argparse import ArgumentParser
import sys
from types import SimpleNamespace

from dynaparse.dynamic_configuration import DynamicConfiguration


class DynamicArgumentParser(ArgumentParser):
    """Extends 'ArgumentParser' to include dynamic functionality."""

    _RESERVED_ARGS = ["spec", "config", "random_sample"]

    def __init__(self, *args, **kwargs):
        """Initialize new arg parser with dynamic args taken into account."""
        super().__init__(*args, **kwargs)

        self._spec_file = self._get_command_line_value_from_arg("spec")
        self._config_file = self._get_command_line_value_from_arg("config")
        self._dynamic_config = DynamicConfiguration(
            config=self._config_file, spec=self._spec_file
        )

        self.add_argument(
            "--spec",
            type=str,
            default=None,
            help="Dynamic configuration spec file specifying metadata for variable named arguments",
        )
        self.add_argument(
            "--config",
            type=str,
            default=None,
            help="File specifying values following the schema in 'spec'. These will override command line args if specified.",
        )
        self.add_argument(
            "--random_sample",
            action="store_true",
            default=False,
            help="If True, generate random parameters from the specified dynamic configuration.",
        )

    def add_argument(self, *args, **kwargs):
        try:
            super().add_argument(*args, **kwargs)
        except argparse.ArgumentError:
            raise Exception(
                "Can't add argument, conflict with reserved args: %s"
                % (self._RESERVED_ARGS)
            )

    def append_config(self, config):
        """Append a new config to the existing configuration. Accepts all inputs that a dynamic configuration accepts."""
        other_dynamic_config = DynamicConfiguration(config=config)
        self._dynamic_config.merge_with(other_dynamic_config, inplace=True)

    def parse_args(self):
        """Parse all arguments including dynamic configuration-based ones."""
        self._merge_dynamic_config_into_argparser()
        args = super().parse_args()

        if args.config is not None:
            self._dynamic_config.overwrite_args_with_contents(args)
        if args.random_sample:
            self._dynamic_config.overwrite_args_with_random(args)
        if self._dynamic_config.has_spec():
            self._dynamic_config.validate_args(args)

        return self._patch_kwargs(args)

    def format_help(self):
        """Format help as usual, but append note about dynamic argument parser."""
        help_str = super().format_help()
        help_str += "\nNOTE: This script uses a dynamic argument parser for configuration.\nSee https://github.com/kungfuai/dynaparse for more information.\n"
        return help_str

    def _get_command_line_value_from_arg(self, arg):
        """Return command line value from a specific argument name."""
        arg_str = "--" + arg
        for i in range(len(sys.argv)):
            if sys.argv[i] == arg_str:
                return sys.argv[i + 1]
        return None

    def _merge_dynamic_config_into_argparser(self):
        """Append arguments for a dynamic configuration."""
        self._dynamic_config.append_to_arg_parser(self)
        self._dynamic_config.patch_sys_argv()

    def _patch_kwargs(self, args):
        """Patch kwargs in an argparse namespace so that nested values are accessible via dot notation."""
        kwargs = args._get_kwargs()

        def assign(parent_obj, parent_names, arg_name, arg_value):
            if len(parent_names) > 0:
                if parent_names[0] not in dir(parent_obj):
                    setattr(parent_obj, parent_names[0], SimpleNamespace())
                curr_parent = parent_names.pop(0)
                assign(
                    getattr(parent_obj, curr_parent), parent_names, arg_name, arg_value
                )
            else:
                setattr(parent_obj, arg_name, arg_value)
                return

        for arg in kwargs:
            arg_full_name = arg[0]
            if "." in arg_full_name:
                arg_value = arg[1]
                parent_names = arg_full_name.split(".")[:-1]
                arg_name = arg_full_name.split(".")[-1]
                assign(args, parent_names, arg_name, arg_value)
                delattr(args, arg_full_name)

        return args
