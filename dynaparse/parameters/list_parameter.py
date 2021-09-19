import json
import random
from dataclasses import dataclass

from dynaparse.parameters.base_parameter import BaseParameter


@dataclass
class ListParameter(BaseParameter):
    default: list
    value_type: str
    parameter_type: str = "list"

    def __post_init__(self):
        """Post-initialization validation method."""

        def cast_dict(raw):
            if isinstance(raw, str):
                return json.loads(raw.replace("'", '"'))
            return raw

        super().__post_init__()
        self.value_typefunc = (
            cast_dict if self.value_type == "dict" else eval(self.value_type)
        )

    def sample(self):
        """Sample at random, but since there's no notion of this, return the default."""
        return self.default

    def get_typefunc(self):
        """Return typefunc for list."""
        return lambda x: [self.value_typefunc(v) for v in x]

    def get_argparse_type(self):
        """Return list."""
        return self.value_typefunc

    def is_list(self):
        """Return whether or not this class is for a list parameter."""
        return True
