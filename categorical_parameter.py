import random
from dataclasses import dataclass

from base_parameter import BaseParameter


@dataclass
class CategoricalParameter(BaseParameter):
    default: str
    options: list
    parameter_type: str = "categorical"

    def __post_init__(self):
        """Post-initialization validation method."""
        if self.default not in self.options:
            raise Exception(
                "Default value '%s' not in options list '%s'"
                % (self.default, str(self.options))
            )

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        return random.choice(self.options)

    def get_typefunc(self):
        """Return str."""

        def cast_type(x):
            casted = str(x)
            if casted not in self.options:
                raise Exception(
                    "Value '%s' not in options list '%s'" % (casted, self.options)
                )
            return casted

        return cast_type

    def get_argparse_type(self):
        """Return str."""
        return str
