from dynaparse.parsers.configuration_file_parser import ConfigurationFileParser
from dynaparse.parameters.boolean_parameter import BooleanParameter
from dynaparse.parameters.categorical_parameter import CategoricalParameter
from dynaparse.parameters.float_parameter import FloatParameter
from dynaparse.parameters.int_parameter import IntParameter
from dynaparse.parameters.list_parameter import ListParameter
from dynaparse.parameters.string_parameter import StringParameter


class SchemaBuilder:
    @classmethod
    def _get_parameter_dict_for_value(cls, name, value):
        """Get a parameter dict given a static value."""
        if isinstance(value, bool):
            param = BooleanParameter(
                name=name, help="(NO HELP CONFIGURED)", required=True, default=value
            )
        elif isinstance(value, int):
            param = IntParameter(
                name=name,
                help="(NO HELP CONFIGURED)",
                required=True,
                default=value,
                p1=value,
                p2=value,
            )
        elif isinstance(value, float):
            param = FloatParameter(
                name=name,
                help="(NO HELP CONFIGURED)",
                required=True,
                default=value,
                p1=value,
                p2=value,
            )
        elif isinstance(value, str):
            param = StringParameter(
                name=name, help="(NO HELP CONFIGURED)", required=True, default=value
            )
        elif isinstance(value, list):
            value_type = cls._get_value_type_from_list(value)
            param = ListParameter(
                name=name,
                help="(NO HELP CONFIGURED)",
                required=True,
                default=value,
                value_type=value_type,
            )
        elif isinstance(value, type(None)):
            param = StringParameter(
                name=name, help="(NO HELP CONFIGURED)", required=True, default=None
            )
        else:
            raise Exception(
                "Can't infer type for variable %s of type %s and value %s"
                % (name, str(type(value)), str(value))
            )
        return param.to_dict()

    @classmethod
    def _get_value_type_from_list(cls, value_list):
        """Get a value type string, inferring from a reference list."""
        if len(value_list) == 0:
            return "str"
        elif isinstance(value_list[0], bool):
            return "bool"
        elif isinstance(value_list[0], int):
            return "int"
        elif isinstance(value_list[0], str):
            return "str"
        elif isinstance(value_list[0], float):
            return "float"
        elif isinstance(value_list[0], dict):
            return "dict"
        else:
            return "str"

    @classmethod
    def infer_from_config_file(cls, filename):
        """Infer schema from a values file."""
        flat_config = ConfigurationFileParser.load_flat_config(filename)
        return cls.infer_from_flat_config(flat_config)

    @classmethod
    def infer_from_flat_config(cls, flat_config):
        inferred_schema = {}
        for key, value in flat_config.items():
            name = key.split(".")[-1]
            inferred_schema[key] = cls._get_parameter_dict_for_value(name, value)
        return inferred_schema
