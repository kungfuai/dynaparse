import pytest
from unittest.mock import Mock

from dynaparse.parameters.base_parameter import BaseParameter


def test_init_when_valid():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    assert bp.name == "test_param"
    assert bp.help == "test_param help"
    assert bp.required


def test_init_when_args_unspecified():
    with pytest.raises(TypeError):
        BaseParameter()


def test_init_when_name_type_invalid():
    with pytest.raises(TypeError):
        BaseParameter(name=1, help="test", required=True)


def test_init_when_help_type_invalid():
    with pytest.raises(TypeError):
        BaseParameter(name="test", help=1, required=True)


def test_init_when_required_type_invalid():
    with pytest.raises(TypeError):
        BaseParameter(name="test", help="test", required=1)


def test_cast_when_int():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    bp.get_typefunc = lambda: int
    assert bp.cast("1") == 1


def test_cast_when_none():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    bp.get_typefunc = lambda: int
    assert bp.cast(None) is None


def test_get_default():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    bp.default = "test"
    assert bp.get_default() == "test"


def test_get_name():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    assert bp.get_name() == "test_param"


def test_get_help():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    assert bp.get_help() == "test_param help"


def test_to_dict():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    assert bp.to_dict() == {
        "name": "test_param",
        "help": "test_param help",
        "required": True,
    }


def test_is_list():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    assert not bp.is_list()


def test_get_argparse_args_when_not_list():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    bp.get_argparse_type = lambda: "test_type"
    bp.get_default = lambda: "test_default"
    assert bp.get_argparse_args() == {
        "type": "test_type",
        "default": "test_default",
        "help": "test_param help",
        "required": True,
    }


def test_get_argparse_args_when_list():
    bp = BaseParameter(name="test_param", help="test_param help", required=True)
    bp.get_argparse_type = lambda: "test_type"
    bp.get_default = lambda: "test_default"
    bp.is_list = lambda: True
    assert bp.get_argparse_args() == {
        "type": "test_type",
        "default": "test_default",
        "help": "test_param help",
        "required": True,
        "nargs": "+",
    }
