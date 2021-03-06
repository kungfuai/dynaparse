from collections import OrderedDict
import json


class ConfigurationFileParser:
    @classmethod
    def load_flat_schema(cls, schema_file):
        """Return the flattened schema dict from JSON file."""
        with open(schema_file, "r") as fd:
            raw_schema = json.load(fd)
        return cls._flatten_nested_structure(raw_schema)

    @classmethod
    def load_flat_values(cls, values_file):
        """Return flattened values dict from JSON file."""
        with open(values_file, "r") as fd:
            raw_values = json.load(fd)
        return cls._flatten_nested_structure(raw_values)

    @classmethod
    def expand_flat_schema(cls, schema_dict):
        """Expand a flattened schema dict."""
        return cls._expand_flat_structure(schema_dict, is_schema=True)

    @classmethod
    def expand_flat_values(cls, values_dict):
        """Expand a flattened values dict."""
        return cls._expand_flat_structure(values_dict, is_schema=False)

    @classmethod
    def _get_parameter_type(cls, raw):
        """Check if dict is a parameter dict."""
        is_parameter_dict = False
        is_parameter_list = False
        is_parameter_value = False
        if isinstance(raw, dict):
            is_parameter_dict = "name" in raw and "help" in raw and "required" in raw
        elif isinstance(raw, list):
            is_parameter_list = not any([isinstance(el, dict) for el in raw])
        else:
            is_parameter_value = True

        if is_parameter_dict:
            return "parameter_dict"
        elif is_parameter_value or is_parameter_list:
            return "parameter_value"
        else:
            return "parent"

    @classmethod
    def _flatten_nested_structure(cls, raw_dict):
        """Flatten the schema dict for argparse interoperability."""
        flat_dict = OrderedDict()

        def extract_flat_parameters(raw, parent_str=None):
            raw_type = cls._get_parameter_type(raw)
            if raw_type == "parameter_value":
                flat_dict[parent_str] = raw
                return
            if isinstance(raw, list):
                for instance in raw:
                    extract_flat_parameters(instance, parent_str)
            elif isinstance(raw, dict):
                if raw_type == "parameter_dict":
                    parameter_name = (
                        raw["name"]
                        if parent_str is None
                        else ".".join([parent_str, raw["name"]])
                    )
                    flat_dict[parameter_name] = raw
                    return
                elif raw_type == "parameter_value":
                    flat_dict[parent_str] = raw
                    return
                for key in raw:
                    new_parent_str = (
                        key if parent_str is None else ".".join([parent_str, key])
                    )
                    extract_flat_parameters(raw[key], new_parent_str)

        extract_flat_parameters(raw_dict)
        return flat_dict

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
    def _expand_flat_structure(cls, structure, is_schema):
        """Expand a flattened schema dict into a serializable nested dict."""
        output_list = []
        nested_dict = OrderedDict()
        for key in structure:
            if "." not in key:
                if is_schema:
                    output_list.append(structure[key])
                else:
                    nested_dict[key] = structure[key]
            else:
                parent_keys = key.split(".")[:-1]
                cls._assign_nested_value_by_keys(
                    nested_dict, parent_keys, structure[key]
                )
        output_list.append(nested_dict)
        return output_list if is_schema else nested_dict
