import random
from dataclasses import dataclass

from base_parameter import BaseParameter


@dataclass
class BooleanParameter(BaseParameter):
    default: bool
    parameter_type: str = "bool"

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        return random.choice([False, True])

    def get_typefunc(self):
        """Return bool."""
        return bool

    def get_argparse_type(self):
        """Return bool."""
        return bool
