from argparse import _StoreAction
from collections import OrderedDict
import json
import os
import sys

from src.config.boolean_parameter import BooleanParameter
from src.config.categorical_parameter import CategoricalParameter
from src.config.float_parameter import FloatParameter
from src.config.int_parameter import IntParameter
from src.config.list_parameter import ListParameter
from src.config.string_parameter import StringParameter


class DynamicConfiguration:
    def __init__(self, values_file=None, schema_file=None):
        """Instantiate new dynamic configuration object."""
        self.values_file = values_file
        self.schema_file = schema_file
        self._schema = OrderedDict()
        self._values = OrderedDict()
        if self.schema_file is not None:
            self.load_schema(self.schema_file)
        if self.values_file is not None:
            self.load_file(values_file)

    def has_schema(self):
        """Return whether schema are loaded."""
        return self.schema_file is not None

    def get_values(self, random=False, fill_defaults=True):
        """Get a dictionary of currently configured values, filling in defaults if required."""
        to_return = {}
        for name in self._schema:
            if not self._schema[name].required and name not in self._values:
                continue
            if random:
                to_return[name] = self._schema[name].sample()
            elif name in self._values:
                to_return[name] = self._values[name]
            elif fill_defaults:
                to_return[name] = self._schema[name].get_default()
        return to_return

    def get_values_as_str(self, random=False, fill_defaults=True):
        """Cast values as strings."""
        to_return = self.get_values(random, fill_defaults)
        for name, value_obj in to_return.items():
            if isinstance(value_obj, list):
                to_return[name] = [str(value) for value in value_obj]
            else:
                to_return[name] = str(value_obj)
        return to_return

    def set_value(self, name, value):
        """Set a parameter's value."""
        if name in self._schema:
            self._values[name] = self._schema[name].cast(value)
        else:
            raise Exception("Parameter name '%s' not recognized in schema" % (name))

    def load_values(self, filename):
        """Load values and schema from a given filename."""
        with open(filename, "r") as fd:
            raw_data = json.load(fd)
        print(raw_data)
        for value_name, value in raw_data.items():
            self.set_value(value_name, value)

    def save_values(self, filename):
        """Save configuration values to a file."""
        with open(filename, "w") as fd:
            to_write = (
                self._values if len(self._values) > 0 else self.get_values(random=False)
            )
            json.dump(to_write, fd, indent=4)

    def save_schema(self, schema_file):
        """Save schema to a directory."""
        self.schema_file = schema_file
        raw_schema = [self._schema[k].to_dict() for k in self._schema]
        with open(schema_file, "w") as fd:
            json.dump(raw_schema, fd, indent=4)

    def load_schema(self, schema_file):
        """Load schema from a directory."""
        self.schema_file = schema_file
        self._schema = OrderedDict()
        with open(self.schema_file, "r") as fd:
            raw_schema = json.load(fd)

        for parameter in raw_schema:
            self._append_parameter_from_dict(parameter)

    def _append_parameter_from_dict(self, parameter_dict):
        """Append a parameter to the schema dictionary."""
        if parameter_dict["parameter_type"] == "int":
            initializer = IntParameter
        elif parameter_dict["parameter_type"] == "float":
            initializer = FloatParameter
        elif parameter_dict["parameter_type"] == "bool":
            initializer = BooleanParameter
        elif parameter_dict["parameter_type"] == "categorical":
            initializer = CategoricalParameter
        elif parameter_dict["parameter_type"] == "list":
            initializer = ListParameter
        elif parameter_dict["parameter_type"] == "str":
            initializer = StringParameter
        else:
            raise Exception(
                "Unrecognized parameter type '%s'" % (parameter_dict["parameter_type"])
            )
        self._schema[parameter_dict["name"]] = initializer(**parameter_dict)

    def append_to_arg_parser(self, arg_parser):
        """Append arguments to an existing argparser."""
        existing_arguments = [arg.dest for arg in arg_parser._get_optional_actions()]
        for schema_name, schema_obj in self._schema.items():
            if schema_name in existing_arguments:
                raise Exception(
                    "Can't add dynamic config '%s', argument already exists" % (k)
                )
            arg_parser.add_argument(
                "--" + schema_name, **schema_obj.get_argparse_args()
            )

    def patch_sys_argv(self):
        """Patch sys to include any values that might have been required."""
        for name, value_str in self.get_values_as_str(
            random=False, fill_defaults=True
        ).items():
            if self._schema[name].required and "--" + name not in sys.argv:
                sys.argv.append("--" + name)
                if isinstance(value_str, list):
                    for v in value_str:
                        sys.argv.append(v)
                else:
                    sys.argv.append(value_str)

    def overwrite_args_with_random(self, args):
        """Overwrite args with randomly sampled values."""
        values = self.get_values(random=True)
        for name, value in values.items():
            setattr(args, name, value)

    def overwrite_args_with_contents(self, args):
        """Overwrite args with contents of this class."""
        values = self.get_values(random=False)
        for name, value in values.items():
            setattr(args, name, value)