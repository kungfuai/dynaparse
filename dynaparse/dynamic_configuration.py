import json
import os
import sys

from dynaparse.parsers.configuration_file_parser import ConfigurationFileParser
from dynaparse.parsers.class_model_parser import ClassModelParser
from dynaparse.parameters.boolean_parameter import BooleanParameter
from dynaparse.parameters.categorical_parameter import CategoricalParameter
from dynaparse.parameters.float_parameter import FloatParameter
from dynaparse.parameters.int_parameter import IntParameter
from dynaparse.parameters.list_parameter import ListParameter
from dynaparse.parameters.string_parameter import StringParameter
from dynaparse.util.schema_builder import SchemaBuilder


class DynamicConfiguration:
    def __init__(self, config=None, spec=None):
        """Instantiate new dynamic configuration object."""
        self.config = config
        self.spec = spec
        self._raw_schema = {}
        self._schema = {}
        self._values = {}
        if self.spec is not None:
            self._load_spec(self.spec)
        if self.config is not None:
            self._load_config(self.config)

    def has_spec(self):
        """Return whether schema are loaded."""
        return self.spec is not None and self._schema

    def get_values(self, random=False, fill_defaults=True, expand=False):
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
        return (
            to_return
            if expand is False
            else ConfigurationFileParser.expand_flat_config(to_return)
        )

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

    def save_config(self, filename):
        """Save configuration values to a file."""
        with open(filename, "w") as fd:
            raw_values_dict = self.get_values(random=False)
            json.dump(
                ConfigurationFileParser.expand_flat_config(raw_values_dict),
                fd,
                indent=4,
            )

    def save_spec(self, filename):
        """Save schema to a directory."""
        self.spec = filename
        expanded = ConfigurationFileParser.expand_flat_spec(self._raw_schema)
        with open(filename, "w") as fd:
            json.dump(expanded, fd, indent=4)

    def merge_with(self, other_dynamic_config, inplace=False):
        """Merge another dynamic config with this one.
        
        If names are duplicated, the new dynamic config will overwrite this one.
        """
        if inplace:
            new_dynamic_config = self
        else:
            new_dynamic_config = DynamicConfiguration()
        new_dynamic_config._raw_schema = {
            **self._raw_schema,
            **other_dynamic_config._raw_schema,
        }
        new_dynamic_config._schema = {
            **self._schema,
            **other_dynamic_config._schema,
        }
        new_dynamic_config._values = {
            **self._values,
            **other_dynamic_config._values,
        }
        return new_dynamic_config

    def _load_config(self, spec):
        """Load values and schema from a given spec."""
        is_file = False
        if isinstance(spec, str) and os.path.isfile(spec):
            is_file = True
            raw_data = ConfigurationFileParser.load_flat_config(spec)
        elif isinstance(spec, dict):
            raw_data = ConfigurationFileParser._flatten_nested_structure(spec)
        else:
            nested_data = ClassModelParser(spec).to_dict()
            raw_data = ConfigurationFileParser._flatten_nested_structure(nested_data)
        if self.spec is None:
            if is_file:
                self._raw_schema = SchemaBuilder.infer_from_config_file(spec)
            else:
                self._raw_schema = SchemaBuilder.infer_from_flat_config(raw_data)
            for parameter_name, parameter_dict in self._raw_schema.items():
                self._append_parameter_from_dict(parameter_name, parameter_dict)
        for value_name, value in raw_data.items():
            self.set_value(value_name, value)

    def _load_spec(self, filename):
        """Load schema from a directory."""
        self.spec = filename
        self._raw_schema = ConfigurationFileParser.load_flat_spec(filename)
        for parameter_name, parameter_dict in self._raw_schema.items():
            self._append_parameter_from_dict(parameter_name, parameter_dict)

    def _append_parameter_from_dict(self, parameter_name, parameter_dict):
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
        self._schema[parameter_name] = initializer(**parameter_dict)

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

    def validate_args(self, args):
        """Validate arg types for previously parsed args."""

        for nested_argname in self._schema:
            try:
                obj = getattr(args, nested_argname)
                self._schema[nested_argname].cast(obj)
            except Exception as e:
                if self._schema[nested_argname].required:
                    raise Exception(e)

    def overwrite_args_with_random(self, args):
        """Overwrite args with randomly sampled values."""
        values = self.get_values(random=True)
        for name, value in values.items():
            setattr(args, name, value)

    def overwrite_args_with_contents(self, args):
        """Overwrite args with contents of this class."""
        values = self.get_values(random=False)
        for name, value in values.items():
            if "--" + name not in sys.argv:
                setattr(args, name, value)
