import argparse
import random
from dataclasses import dataclass

from dynaparse.parameters.base_parameter import BaseParameter


def str2bool(v):
    if isinstance(v, bool):
        return v

    if v == "None":
        return None
    elif v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


@dataclass
class BooleanParameter(BaseParameter):
    default: bool
    parameter_type: str = "bool"
    is_constant: bool = True

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        return self.default if self.is_constant else random.choice([False, True])

    def get_typefunc(self):
        """Return bool."""
        return bool

    def get_argparse_type(self):
        """Return bool."""
        return str2bool
