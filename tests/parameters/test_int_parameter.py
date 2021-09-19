import pytest
import random

from dynaparse.parameters.int_parameter import IntParameter
from dynaparse.parameters.int_parameter import int_with_none

BASE_KWARGS = {"name": "test_int", "help": "test_help", "required": True}


def test_init_when_valid():
    ip = IntParameter(
        default=1, distribution="test", p1=2, p2=3, parameter_type="int", **BASE_KWARGS
    )
    assert ip.default == 1
    assert ip.distribution == "test"
    assert ip.p1 == 2
    assert ip.p2 == 3
    assert ip.parameter_type == "int"
    assert ip.name == "test_int"
    assert ip.help == "test_help"
    assert ip.required is True


def test_init_when_invalid_type():
    with pytest.raises(TypeError):
        IntParameter(
            default="1",
            distribution="test",
            p1=2,
            p2=3,
            parameter_type="int",
            **BASE_KWARGS
        )


def test_sample_when_uniform():
    random.seed(0)
    ip = IntParameter(
        default=1,
        distribution="uniform",
        p1=2,
        p2=3,
        parameter_type="int",
        **BASE_KWARGS
    )
    assert ip.sample() == 3


def test_sample_when_distribution_invalid():
    with pytest.raises(Exception):
        IntParameter(
            default=1,
            distribution="test",
            p1=2,
            p2=3,
            parameter_type="int",
            **BASE_KWARGS
        ).sample()


def test_get_typefunc():
    ip = IntParameter(
        default=1,
        distribution="uniform",
        p1=2,
        p2=3,
        parameter_type="int",
        **BASE_KWARGS
    )
    assert ip.get_typefunc() == int_with_none


def test_get_argparse_type():
    ip = IntParameter(
        default=1,
        distribution="uniform",
        p1=2,
        p2=3,
        parameter_type="int",
        **BASE_KWARGS
    )
    assert ip.get_argparse_type() == int_with_none
