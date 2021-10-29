import enum
from pydantic import BaseModel


class EntityType(enum.Enum):
    PERSON = "person"
    ORGANIZATION = "organization"


class ComponentConfigClass1(BaseModel):
    name: str = "a"
    size: int = 3
    entity_type: EntityType = EntityType.PERSON


class ComponentConfigClass2(BaseModel):
    name: str = "b"
    height: int = 4
    component1: ComponentConfigClass1 = ComponentConfigClass1()


class ConfigClassExample(BaseModel):
    param1: int = 1
    param2: float = 2.0
    param3: str = "3"

    component: ComponentConfigClass2 = ComponentConfigClass2()
