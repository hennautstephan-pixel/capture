from pytest import raises

from capture_recovery.discovery import RangeConstraint


def test_name():

    constraint = RangeConstraint(0, 255)

    assert constraint.name == "RangeConstraint"


def test_matches_inside():

    constraint = RangeConstraint(0, 255)

    assert constraint.matches(0)
    assert constraint.matches(42)
    assert constraint.matches(255)


def test_matches_outside():

    constraint = RangeConstraint(0, 255)

    assert not constraint.matches(-1)
    assert not constraint.matches(256)


def test_matches_non_numeric():

    constraint = RangeConstraint(0, 255)

    assert not constraint.matches("42")
    assert not constraint.matches(None)


def test_invalid_range():

    with raises(ValueError):
        RangeConstraint(10, 5)