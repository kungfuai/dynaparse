import random
from dataclasses import dataclass

from src.config.base_parameter import BaseParameter


@dataclass
class IntParameter(BaseParameter):
    default: int = None
    low: int = None
    high: int = None
    distribution: str = "uniform"
    parameter_type: str = "int"

    def __post_init__(self):
        """Post-initialization validation method."""
        super().__post_init__()
        if self.default < self.low or self.default > self.high:
            raise Exception(
                "Default value %d not between low value %d and high value %d (inclusive)"
                % (self.default, self.low, self.high)
            )

    def sample(self):
        """Sample a value from the pre-configured distribution."""
        if self.distribution == "uniform":
            return random.sample(list(range(self.low, self.high + 1)), k=1)[0]

        raise Exception("Unsupported distribution '%s'" % (self.distribution))

    def get_typefunc(self):
        """Return int."""
        return int

    def get_argparse_type(self):
        """Return int."""
        return int