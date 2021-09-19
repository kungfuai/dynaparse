import random
from dataclasses import dataclass

from dynaparse.parameters.base_parameter import BaseParameter

int_with_none = lambda x: None if x == "None" else int(x)


@dataclass
class IntParameter(BaseParameter):
    default: int = None
    distribution: str = "uniform"
    parameter_type: str = "int"
    p1: int = None
    p2: int = None

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        if self.distribution == "uniform":
            return random.sample(list(range(self.p1, self.p2 + 1)), k=1)[0]

        raise Exception("Unsupported distribution '%s'" % (self.distribution))

    def get_typefunc(self):
        """Return int."""
        return int_with_none

    def get_argparse_type(self):
        """Return int."""
        return int_with_none
