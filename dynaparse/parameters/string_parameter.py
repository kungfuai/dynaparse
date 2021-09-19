import random
from dataclasses import dataclass

import numpy as np

from dynaparse.parameters.base_parameter import BaseParameter

str_with_none = lambda x: None if x == "None" else str(x)


@dataclass
class StringParameter(BaseParameter):
    default: str = None
    parameter_type: str = "str"

    def get_typefunc(self):
        """Return str."""
        return str_with_none

    def get_argparse_type(self):
        """Return str."""
        return str_with_none

    def sample(self):
        """Return a random sample, but since there's no notion of sampling, return default value."""
        return self.default
