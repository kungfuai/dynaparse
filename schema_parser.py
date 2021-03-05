from collections import OrderedDict
import json


class SchemaParser:
    @classmethod
    def load_flat_schema(cls, schema_file):
        """Return the flattened schema dict."""
        with open(schema_file, "r") as fd:
            raw_schema = json.load(fd)
        return cls._flatten_schema_dict(raw_schema)

    @classmethod
    def _is_parameter_dict(cls, raw_dict):
        """Check if dict is a parameter dict."""
        return "name" in raw_dict and "help" in raw_dict and "required" in raw_dict

    @classmethod
    def _flatten_schema_dict(cls, raw_schema):
        """Flatten the schema dict for argparse interoperability."""
        flat_schema = OrderedDict()

        def extract_flat_parameters(raw, parent_str=None):
            if isinstance(raw, list):
                for instance in raw:
                    extract_flat_parameters(instance, parent_str)
            elif isinstance(raw, dict):
                if cls._is_parameter_dict(raw):
                    parameter_name = (
                        raw["name"]
                        if parent_str is None
                        else ".".join([parent_str, raw["name"]])
                    )
                    flat_schema[parameter_name] = raw
                    return
                for key in raw:
                    parent_str = (
                        key if parent_str is None else ".".join([parent_str, key])
                    )
                    extract_flat_parameters(raw[key], parent_str)

        extract_flat_parameters(raw_schema)
        return flat_schema

    @classmethod
    def _assign_nested_value_by_keys(cls, output_dict, parent_keys, value):
        """Assign a value into a nested dict, creating keys as necessary."""

        def assign(curr_dict, remaining_keys):
            key = remaining_keys[0]
            if len(remaining_keys) == 1:
                if key not in curr_dict:
                    curr_dict[key] = []
                curr_dict[key].append(value)
                return
            else:
                if key not in curr_dict:
                    curr_dict[key] = OrderedDict()
                assign(curr_dict[key], remaining_keys[1:])

        assign(output_dict, parent_keys)

    @classmethod
    def expand_flat_schema_dict(cls, schema_dict):
        """Expand a flattened schema dict into a serializable nested dict."""
        output_list = []
        nested_dict = OrderedDict()
        for key in schema_dict:
            if "." not in key:
                output_list.append(schema_dict[key])
            else:
                parent_keys = key.split(".")[:-1]
                cls._assign_nested_value_by_keys(
                    nested_dict, parent_keys, schema_dict[key]
                )
        output_list.append(nested_dict)
        return output_list
