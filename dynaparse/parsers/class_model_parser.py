import importlib

from pydantic import BaseModel
import yaml


class ClassModelParser:
    def __init__(self, obj):
        if isinstance(obj, str):
            self.model = self._load_from_path(obj)
        elif isinstance(obj, BaseModel):
            self.model = obj
        else:
            raise Exception(
                "Unrecognized class %s, can't parse with ClassModelParser" % str(obj)
            )

    def _load_from_path(self, path):
        """Load an enum class given an import path."""
        base_path = ".".join(path.split(".")[:-1])
        class_name = path.split(".")[-1]
        return getattr(importlib.import_module(base_path), class_name)()

    def to_dict(self):
        """Generate (potentially nested) dictionary from pydantic base model config class."""
        if isinstance(self.model, BaseModel):
            return self.model.dict()
        else:
            return yaml.safe_load(self.model.__doc__)
