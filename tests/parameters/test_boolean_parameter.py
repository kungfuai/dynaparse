import argparse
import pytest
import random

from dynaparse.parameters.boolean_parameter import BooleanParameter
from dynaparse.parameters.boolean_parameter import str2bool

BASE_KWARGS = {"name": "test_bool", "help": "test_help", "required": True}


def test_str2bool_when_boolean():
    assert str2bool(True) is True
    assert not str2bool(False) is True


def test_str2bool_when_str_and_true():
    assert str2bool("yes") is True
    assert str2bool("true") is True
    assert str2bool("t") is True
    assert str2bool("y") is True
    assert str2bool("1") is True


def test_str2bool_when_str_and_false():
    assert str2bool("no") is False
    assert str2bool("false") is False
    assert str2bool("f") is False
    assert str2bool("n") is False
    assert str2bool("0") is False


def test_str2bool_when_unrecognized():
    with pytest.raises(argparse.ArgumentTypeError):
        str2bool("test")


def test_init_when_valid():
    bp = BooleanParameter(default=True, **BASE_KWARGS)
    assert bp.default is True
    assert bp.parameter_type == "bool"
    assert bp.is_constant is True


def test_init_when_invalid_default():
    with pytest.raises(TypeError):
        BooleanParameter(default="test", **BASE_KWARGS)


def test_init_when_invalid_parameter_type():
    with pytest.raises(TypeError):
        BooleanParameter(default=True, parameter_type=1, **BASE_KWARGS)


def test_init_when_invalid_is_constant_type():
    with pytest.raises(TypeError):
        BooleanParameter(default=True, is_constant=None, **BASE_KWARGS)


def test_sample_when_true():
    bp = BooleanParameter(default=True, is_constant=False, **BASE_KWARGS)
    random.seed(0)
    assert bp.sample() is True


def test_sample_when_false():
    bp = BooleanParameter(default=True, is_constant=False, **BASE_KWARGS)
    random.seed(1)
    assert bp.sample() is False


def test_sample_when_is_constant():
    bp = BooleanParameter(default=True, is_constant=True, **BASE_KWARGS)
    random.seed(1)
    assert bp.sample() is True


def test_get_typefunc():
    bp = BooleanParameter(default=True, **BASE_KWARGS)
    assert bp.get_typefunc() == bool


def test_get_argparse_type():
    bp = BooleanParameter(default=True, **BASE_KWARGS)
    assert bp.get_argparse_type() == str2bool
