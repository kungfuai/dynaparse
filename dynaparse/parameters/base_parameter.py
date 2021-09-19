from dataclasses import asdict, dataclass

from typeguard import check_type


@dataclass
class BaseParameter:
    name: str
    help: str
    required: bool

    def __post_init__(self):
        """Validate the input."""
        for parameter, field in self.__dataclass_fields__.items():
            try:
                check_type(parameter, getattr(self, parameter), field.type)
            except TypeError:
                if getattr(self, parameter) is not None:
                    raise TypeError(
                        "Parameter '%s' (value: '%s') type invalid, should be '%s'"
                        % (parameter, str(getattr(self, parameter)), str(field.type))
                    )

    def cast(self, value):
        """Cast a value type 'int'."""
        if value in [None, "None"]:
            return None
        try:
            return self.get_typefunc()(value)
        except Exception as e:
            raise Exception(
                "Exception encountered while typecasting parameter '%s' with value '%s'"
                % (self.name, str(value))
            )

    def get_default(self):
        """Return the default value."""
        return self.default

    def get_name(self):
        """Return the name of the parameter."""
        return self.name

    def get_help(self):
        """Return help string for the parameter."""
        return self.help

    def to_dict(self):
        """Return a dictionary representation of this class."""
        return asdict(self)

    def is_list(self):
        """Default base class to 'not a list'."""
        return False

    def get_argparse_args(self):
        """Return a dictionary of argparse args."""
        args = {
            "type": self.get_argparse_type(),
            "default": self.get_default(),
            "help": self.get_help(),
            "required": self.required,
        }
        if self.is_list():
            args["nargs"] = "+"
        return args
