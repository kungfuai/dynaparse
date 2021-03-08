import json


class ConfigurationFileParser:
    @classmethod
    def load_flat_metaconfig(cls, filename):
        """Return the flattened metaconfig dict from JSON file."""
        with open(filename, "r") as fd:
            raw = json.load(fd)
        return cls._flatten_nested_structure(raw)

    @classmethod
    def load_flat_config(cls, filename):
        """Return flattened config dict from JSON file."""
        with open(filename, "r") as fd:
            raw = json.load(fd)
        return cls._flatten_nested_structure(raw)

    @classmethod
    def expand_flat_metaconfig(cls, metaconfig_dict):
        """Expand a flattened metaconfig dict."""
        return cls._expand_flat_structure(metaconfig_dict, is_metaconfig=True)

    @classmethod
    def expand_flat_config(cls, config_dict):
        """Expand a flattened config dict."""
        return cls._expand_flat_structure(config_dict, is_metaconfig=False)

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
        """Flatten dict structure for argparse interoperability."""
        flat_dict = {}

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
    def _assign_nested_value_by_keys(
        cls, output_dict, parent_keys, value, is_metaconfig
    ):
        """Assign a value into a nested dict, creating keys as necessary."""

        def assign(curr_dict, remaining_keys):
            key = remaining_keys[0]
            if len(remaining_keys) == 1:
                if is_metaconfig:
                    if key not in curr_dict:
                        curr_dict[key] = []
                    curr_dict[key].append(value)
                else:
                    curr_dict[key] = value
                return
            else:
                if key not in curr_dict:
                    curr_dict[key] = {}
                assign(curr_dict[key], remaining_keys[1:])

        assign(output_dict, parent_keys)

    @classmethod
    def _expand_flat_structure(cls, structure, is_metaconfig):
        """Expand a flattened data structure into a serializable nested dict."""
        output_list = []
        nested_dict = {}
        for key in structure:
            if "." not in key:
                if is_metaconfig:
                    output_list.append(structure[key])
                else:
                    nested_dict[key] = structure[key]
            else:
                parent_keys = key.split(".")
                cls._assign_nested_value_by_keys(
                    nested_dict, parent_keys, structure[key], is_metaconfig
                )
        output_list.append(nested_dict)
        return output_list if is_metaconfig else nested_dict
