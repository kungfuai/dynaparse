import pytest

import numpy as np

from dynaparse.parameters.float_parameter import FloatParameter
from dynaparse.parameters.float_parameter import float_with_none

BASE_KWARGS = {"name": "test_float", "help": "test_help", "required": True}


def test_init_when_valid():
    fp = FloatParameter(
        default=1.0,
        distribution="test",
        p1=2.0,
        p2=3.0,
        parameter_type="float",
        **BASE_KWARGS
    )
    assert fp.default == 1.0
    assert fp.distribution == "test"
    assert fp.p1 == 2.0
    assert fp.p2 == 3.0
    assert fp.parameter_type == "float"
    assert fp.name == "test_float"
    assert fp.help == "test_help"
    assert fp.required is True


def test_init_when_invalid_type():
    with pytest.raises(TypeError):
        FloatParameter(
            default="1.0",
            distribution="test",
            p1=2.0,
            p2=3.0,
            parameter_type="float",
            **BASE_KWARGS
        )


def test_sample_when_uniform():
    fp = FloatParameter(
        default=1.0,
        distribution="uniform",
        p1=2.0,
        p2=3.0,
        parameter_type="float",
        **BASE_KWARGS
    )
    np.random.seed(0)
    assert np.isclose(fp.sample(), 2.5488135039273248)


def test_sample_when_normal():
    fp = FloatParameter(
        default=1.0,
        distribution="normal",
        p1=2.0,
        p2=3.0,
        parameter_type="float",
        **BASE_KWARGS
    )
    np.random.seed(0)
    assert np.isclose(fp.sample(), 7.292157037902992)


def test_sample_when_distribution_invalid():
    with pytest.raises(Exception):
        FloatParameter(
            default=1.0,
            distribution="test",
            p1=2.0,
            p2=3.0,
            parameter_type="float",
            **BASE_KWARGS
        ).sample()


def test_get_typefunc():
    fp = FloatParameter(
        default=1.0,
        distribution="test",
        p1=2.0,
        p2=3.0,
        parameter_type="float",
        **BASE_KWARGS
    )
    assert fp.get_typefunc() == float_with_none


def test_get_argparse_type():
    fp = FloatParameter(
        default=1.0,
        distribution="test",
        p1=2.0,
        p2=3.0,
        parameter_type="float",
        **BASE_KWARGS
    )
    assert fp.get_argparse_type() == float_with_none
