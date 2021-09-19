from pydantic import BaseModel


class ConfigClassExample(BaseModel):
    param1: int = 1
    param2: float = 2.0
    param3: str = "3"
