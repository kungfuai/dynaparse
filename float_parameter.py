import random
from dataclasses import dataclass

import numpy as np

from base_parameter import BaseParameter


@dataclass
class FloatParameter(BaseParameter):
    default: float = None
    low: float = None
    high: float = None
    distribution: str = "uniform"
    parameter_type: str = "float"

    def __post_init__(self):
        """Post-initialization validation method."""
        super().__post_init__()
        if self.default < self.low or self.default > self.high:
            raise Exception(
                "Default value %f not between low value %f and high value %f (inclusive)"
                % (self.default, self.low, self.high)
            )

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        if self.distribution == "uniform":
            return np.random.uniform(low=self.low, high=self.high, size=1)[0]

        raise Exception("Unsupported distribution '%s'" % (self.distribution))

    def get_typefunc(self):
        """Return float."""
        return float

    def get_argparse_type(self):
        """Return float."""
        return float
