import pytest

from dynaparse.parameters.string_parameter import StringParameter


BASE_KWARGS = {"name": "test_string", "help": "test_help", "required": True}


def test_init_when_valid():
    sp = StringParameter(default="stringval", parameter_type="string", **BASE_KWARGS)
    assert sp.default == "stringval"
    assert sp.parameter_type == "string"
    assert sp.name == "test_string"
    assert sp.help == "test_help"
    assert sp.required is True


def test_init_when_invalid_type():
    with pytest.raises(TypeError):
        StringParameter(1, parameter_type="string", **BASE_KWARGS)


def test_get_typefunc():
    sp = StringParameter(default="stringval", parameter_type="string", **BASE_KWARGS)
    assert sp.get_typefunc() == str


def test_get_argparse_type():
    sp = StringParameter(default="stringval", parameter_type="string", **BASE_KWARGS)
    assert sp.get_argparse_type() == str


def test_sample():
    sp = StringParameter(default="stringval", parameter_type="string", **BASE_KWARGS)
    assert sp.sample() == "stringval"
    assert sp.sample() == "stringval"  # Run multiple times
