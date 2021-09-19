import json

from dynaparse.parsers.yaml_parser import YAMLParser


class ConfigurationFileParser:
    @classmethod
    def load_flat_spec(cls, filename):
        """Return the flattened spec dict from JSON file."""
        with open(filename, "r") as fd:
            raw = json.load(fd)
        return cls._flatten_nested_structure(raw)

    @classmethod
    def load_flat_config(cls, filename):
        """Return flattened config dict from JSON file."""
        if YAMLParser.is_yaml(filename):
            raw = YAMLParser.load(filename)
        else:  # Assume json otherwise
            with open(filename, "r") as fd:
                raw = json.load(fd)
        return cls._flatten_nested_structure(raw)

    @classmethod
    def expand_flat_spec(cls, spec_dict):
        """Expand a flattened spec dict."""
        return cls._expand_flat_structure(spec_dict, is_spec=True)

    @classmethod
    def expand_flat_config(cls, config_dict):
        """Expand a flattened config dict."""
        return cls._expand_flat_structure(config_dict, is_spec=False)

    @classmethod
    def _is_parameter_dict(cls, raw):
        """Check if a dictionary refers to a parameter."""
        return isinstance(raw, dict) and (
            "name" in raw and "help" in raw and "required" in raw and "default" in raw
        )

    @classmethod
    def _get_parameter_type(cls, raw):
        """Check if dict is a parameter dict."""
        is_parameter_dict = False
        is_parameter_list = False
        is_parameter_value = False
        if isinstance(raw, dict):
            is_parameter_dict = cls._is_parameter_dict(raw)
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
    def _has_parameter_children(cls, raw):
        """Check whether a nested structure has parameter children."""

        def inspect(to_inspect):
            found_parameter = False
            found_child_parameter = False
            if isinstance(to_inspect, list):
                for el in to_inspect:
                    found_child_parameter = inspect(el)
            elif isinstance(to_inspect, dict):
                if cls._is_parameter_dict(to_inspect):
                    found_parameter = True
                for _, value in to_inspect.items():
                    if isinstance(value, list) or isinstance(value, dict):
                        found_child_parameter = inspect(value)
            return found_parameter or found_child_parameter

        return inspect(raw)

    @classmethod
    def _is_kwarg_list(cls, raw):
        """Check if a list contains kwargs, e.g. for augmentation config."""
        if not isinstance(raw, list):
            return False
        if not all([isinstance(el, dict)] for el in raw):
            return False
        if all([cls._is_parameter_dict(el) for el in raw]):
            return False
        if cls._has_parameter_children(raw):
            return False
        return True

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
                if cls._is_kwarg_list(raw):
                    flat_dict[parent_str] = raw
                    return
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
    def _assign_nested_value_by_keys(cls, output_dict, parent_keys, value, is_spec):
        """Assign a value into a nested dict, creating keys as necessary."""

        def assign(current, remaining_keys):
            key = remaining_keys[0]
            if is_spec and len(remaining_keys) == 2:
                if key not in current:
                    current[key] = []
                current[key].insert(-1, value)
                return
            elif not is_spec and len(remaining_keys) == 1:
                current[key] = value
                return
            else:
                if is_spec:
                    if key not in current:
                        current[key] = []
                    if (
                        len(current[key]) == 0
                        or cls._get_parameter_type(current[key][-1]) == "parameter_dict"
                    ):
                        current[key].append({})
                    assign(current[key][-1], remaining_keys[1:])
                else:
                    if key not in current:
                        current[key] = {}
                    assign(current[key], remaining_keys[1:])

        assign(output_dict, parent_keys)

    @classmethod
    def _expand_flat_structure(cls, structure, is_spec):
        """Expand a flattened data structure into a serializable nested dict."""
        output_list = []
        nested_dict = {}
        for key in structure:
            if "." not in key:
                if is_spec:
                    output_list.append(structure[key])
                else:
                    nested_dict[key] = structure[key]
            else:
                parent_keys = key.split(".")
                cls._assign_nested_value_by_keys(
                    nested_dict, parent_keys, structure[key], is_spec
                )
        if len(nested_dict) > 0:
            output_list.append(nested_dict)
        return output_list if is_spec else nested_dict
