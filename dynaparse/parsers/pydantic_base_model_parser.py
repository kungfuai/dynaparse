import importlib

from pydantic import BaseModel


class PydanticBaseModelParser:
    def __init__(self, obj):
        if isinstance(obj, BaseModel):
            self.base_model = obj
        elif isinstance(obj, str):
            self.base_model = self._load_from_path(obj)

    def _load_from_path(self, path):
        """Load an enum class given an import path."""
        base_path = ".".join(path.split(".")[:-1])
        class_name = path.split(".")[-1]
        return getattr(importlib.import_module(base_path), class_name)()

    def to_dict(self):
        """Generate (potentially nested) dictionary from pydantic base model config class."""
        return self.base_model.dict()
