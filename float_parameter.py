import random
from dataclasses import dataclass

import numpy as np

from base_parameter import BaseParameter


@dataclass
class FloatParameter(BaseParameter):
    default: float = None
    distribution: str = "uniform"
    p1: float = None
    p2: float = None
    parameter_type: str = "float"

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        if self.distribution == "uniform":
            return np.random.uniform(low=self.p1, high=self.p2, size=1)[0]
        elif self.distribution == "normal":
            return np.random.normal(loc=self.p1, scale=self.p2, size=1)[0]

        raise Exception("Unsupported distribution '%s'" % (self.distribution))

    def get_typefunc(self):
        """Return float."""
        return float

    def get_argparse_type(self):
        """Return float."""
        return float
