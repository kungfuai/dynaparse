from dynaparse.parameters.list_parameter import ListParameter


BASE_KWARGS = {"name": "test_list", "help": "test_help", "required": True}


def test_init_when_valid_int():
    lp = ListParameter(
        default=[1, 2, 3], value_type="int", parameter_type="list", **BASE_KWARGS
    )
    assert lp.default == [1, 2, 3]
    assert all([isinstance(v, int) for v in lp.default])
    assert lp.value_typefunc == int
    assert lp.value_type == "int"
    assert lp.parameter_type == "list"
    assert lp.name == "test_list"
    assert lp.help == "test_help"
    assert lp.required is True


def test_init_when_valid_float():
    lp = ListParameter(
        default=[1.0, 2.0, 3.0],
        value_type="float",
        parameter_type="list",
        **BASE_KWARGS
    )
    assert lp.default == [1.0, 2.0, 3.0]
    assert all([isinstance(v, float) for v in lp.default])
    assert lp.value_typefunc == float
    assert lp.value_type == "float"
    assert lp.parameter_type == "list"
    assert lp.name == "test_list"
    assert lp.help == "test_help"
    assert lp.required is True


def test_that_sample_returns_default():
    lp = ListParameter(
        default=[1, 2, 3], value_type="int", parameter_type="list", **BASE_KWARGS
    )
    assert lp.sample() == [1, 2, 3]
    assert lp.sample() == [1, 2, 3]  # Check multiple times


def test_get_typefunc_when_int():
    lp = ListParameter(
        default=[1, 2, 3], value_type="int", parameter_type="list", **BASE_KWARGS
    )
    typed = lp.get_typefunc()(["1", "2", "3"])
    assert typed == [1, 2, 3]
    assert all([isinstance(v, int) for v in typed])


def test_get_argparse_type_when_int():
    lp = ListParameter(
        default=[1, 2, 3], value_type="int", parameter_type="list", **BASE_KWARGS
    )
    assert lp.get_argparse_type() == int


def test_get_argparse_type_when_float():
    lp = ListParameter(
        default=[1, 2, 3], value_type="float", parameter_type="list", **BASE_KWARGS
    )
    assert lp.get_argparse_type() == float


def test_is_list():
    lp = ListParameter(
        default=[1, 2, 3], value_type="float", parameter_type="list", **BASE_KWARGS
    )
    assert lp.is_list() is True
