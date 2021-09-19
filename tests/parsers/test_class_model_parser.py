import pytest
from unittest.mock import patch

from dynaparse.parsers.class_model_parser import ClassModelParser
from tests.data.config_class_example import ConfigClassExample


def test_init_when_dot_notation_file():
    with patch(
        "dynaparse.parsers.class_model_parser.ClassModelParser._load_from_path"
    ) as patched_class_load:
        patched_class_load.return_value = "test"
        parser = ClassModelParser("tests.data.config_class_example.ConfigClassExample")
        assert patched_class_load.call_count == 1
        assert parser.model == "test"


def test_init_when_class():
    in_class = ConfigClassExample()
    parser = ClassModelParser(in_class)
    assert parser.model == in_class


def test_init_when_unparseable():
    with pytest.raises(Exception):
        ClassModelParser("invalid")


def test_to_dict_when_pydantic():
    in_class = ConfigClassExample()
    parser = ClassModelParser(in_class)
    assert parser.to_dict() == in_class.dict()


def test_load_from_path():
    parser = ClassModelParser("tests.data.config_class_example.ConfigClassExample")
    assert isinstance(
        parser._load_from_path("tests.data.config_class_example.ConfigClassExample"),
        ConfigClassExample,
    )
