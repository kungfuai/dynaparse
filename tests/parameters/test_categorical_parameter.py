import pytest
import random

from dynaparse.parameters.categorical_parameter import CategoricalParameter

BASE_KWARGS = {"name": "test_bool", "help": "test_help", "required": True}


def test_init_when_valid():
    cp = CategoricalParameter(default="o1", options=["o1", "o2"], **BASE_KWARGS)
    assert cp.name == "test_bool"
    assert cp.help == "test_help"
    assert cp.required is True
    assert cp.default == "o1"
    assert cp.options == ["o1", "o2"]


def test_init_when_invalid_option():
    with pytest.raises(Exception):
        CategoricalParameter(default="invalid", options=["o1", "o2"], **BASE_KWARGS)


def test_init_when_invalid_default_type():
    with pytest.raises(TypeError):
        CategoricalParameter(default=1, options=["o1", "o2"], **BASE_KWARGS)


def test_init_when_invalid_options_type():
    with pytest.raises(TypeError):
        CategoricalParameter(default="o1", options=1, **BASE_KWARGS)


def test_sample_when_option_1():
    cp = CategoricalParameter(default="o1", options=["o1", "o2"], **BASE_KWARGS)
    random.seed(1)
    assert cp.sample() == "o1"


def test_sample_when_option_2():
    cp = CategoricalParameter(default="o1", options=["o1", "o2"], **BASE_KWARGS)
    random.seed(0)
    assert cp.sample() == "o2"


def test_typefunc():
    cp = CategoricalParameter(default="o1", options=["o1", "o2"], **BASE_KWARGS)
    typefunc = cp.get_typefunc()
    assert typefunc("o1") == "o1"
    assert typefunc("o2") == "o2"
    with pytest.raises(Exception):
        typefunc("invalid")


def test_get_argparse_type():
    cp = CategoricalParameter(default="o1", options=["o1", "o2"], **BASE_KWARGS)
    assert cp.get_argparse_type() == str
