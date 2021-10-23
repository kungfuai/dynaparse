import warnings

from dynaparse import DynamicConfiguration

test_config_1 = {"A": 1, "B": "Btest", "C": [3, 4, 5], "nested": {"AA": 11}}
test_config_2 = {"C": 6, "D": "Dtest"}


def test_init():
    dc = DynamicConfiguration(config=test_config_1)
    assert dc.get_values() == {"A": 1, "B": "Btest", "C": [3, 4, 5], "nested.AA": 11}
    assert len(dc.get_values()) == 4


def test_merge_when_inplace():
    dc = DynamicConfiguration(config=test_config_1)
    dc2 = DynamicConfiguration(config=test_config_2)
    dc3 = dc.merge_with(dc2, inplace=True)
    assert dc.get_values() == {
        "A": 1,
        "B": "Btest",
        "C": 6,
        "D": "Dtest",
        "nested.AA": 11,
    }
    assert len(dc.get_values()) == 5
    assert dc2.get_values() == {"C": 6, "D": "Dtest"}
    assert len(dc2.get_values()) == 2
    assert dc3.get_values() == {
        "A": 1,
        "B": "Btest",
        "C": 6,
        "D": "Dtest",
        "nested.AA": 11,
    }
    assert len(dc3.get_values()) == 5


def test_merge_when_not_inplace():
    dc = DynamicConfiguration(config=test_config_1)
    dc2 = DynamicConfiguration(config=test_config_2)
    dc3 = dc.merge_with(dc2, inplace=False)
    assert dc.get_values() == {
        "A": 1,
        "B": "Btest",
        "C": [3, 4, 5],
        "nested.AA": 11,
    }
    assert len(dc.get_values()) == 4
    assert dc2.get_values() == {"C": 6, "D": "Dtest"}
    assert len(dc2.get_values()) == 2
    assert dc3.get_values() == {
        "A": 1,
        "B": "Btest",
        "C": 6,
        "D": "Dtest",
        "nested.AA": 11,
    }
    assert len(dc3.get_values()) == 5
