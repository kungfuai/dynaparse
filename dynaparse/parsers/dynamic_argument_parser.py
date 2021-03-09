from argparse import ArgumentParser
import sys
from types import SimpleNamespace

from dynaparse.dynamic_configuration import DynamicConfiguration


class DynamicArgumentParser(ArgumentParser):
    """Extends 'ArgumentParser' to include dynamic functionality."""

    _RESERVED_ARGS = ["metaconfig", "config", "randomize_config"]

    def __init__(self, *args, **kwargs):
        """Initialize new arg parser with dynamic args taken into account."""
        super().__init__(*args, **kwargs)

        self._dynamic_config = DynamicConfiguration()
        self._metaconfig_file = self._get_command_line_value_from_arg("metaconfig")
        self._config_file = self._get_command_line_value_from_arg("config")

        if self._argument_conflicts_exist():
            raise Exception(
                "The following arguments are reserved for the DynamicArgumentParser: %s"
                % (self._RESERVED_ARGS)
            )

        self.add_argument(
            "--metaconfig",
            type=str,
            default=None,
            help="Dynamic configuration metaconfig file specifying metadata for variable named arguments",
        )
        self.add_argument(
            "--config",
            type=str,
            default=None,
            help="File specifying values following the schema in 'metaconfig'. These will override command line args if specified.",
        )
        self.add_argument(
            "--randomize_config",
            action="store_true",
            default=False,
            help="If True, generate random parameters from the specified dynamic configuration.",
        )
        self._check_for_dynamic_config()

    def _get_command_line_value_from_arg(self, arg):
        """Return command line value from a specific argument name."""
        arg_str = "--" + arg
        for i in range(len(sys.argv)):
            if sys.argv[i] == arg_str:
                return sys.argv[i + 1]
        return None

    def _check_for_dynamic_config(self):
        """Append arguments for a dynamic configuration."""
        if self._metaconfig_file is not None:
            self._dynamic_config.load_metaconfig(self._metaconfig_file)
        if self._config_file is not None:
            self._dynamic_config.load_config(self._config_file)
        self._dynamic_config.append_to_arg_parser(self)
        self._dynamic_config.patch_sys_argv()

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
        help_str += "\nNOTE: This script uses a dynamic argument parser for configuration.\nSee https://github.com/kungfuai/dynaparse for more information.\n"
        return help_str

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

    def parse_args(self):
        """Parse all arguments including dynamic configuration-based ones."""
        args = super().parse_args()

        if self._dynamic_config.has_metaconfig() and args.randomize_config:
            self._dynamic_config.overwrite_args_with_random(args)

        if args.config is not None:
            self._dynamic_config.overwrite_args_with_contents(args)

        return self._patch_kwargs(args)