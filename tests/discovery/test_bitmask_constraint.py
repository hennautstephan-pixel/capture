from pytest import raises

from capture_recovery.discovery import BitmaskConstraint


def test_name():

    constraint = BitmaskConstraint(0x0F)

    assert constraint.name == "BitmaskConstraint"


def test_matches_single_bits():

    constraint = BitmaskConstraint(0x0F)

    assert constraint.matches(0)
    assert constraint.matches(1)
    assert constraint.matches(2)
    assert constraint.matches(4)
    assert constraint.matches(8)


def test_matches_combined_bits():

    constraint = BitmaskConstraint(0x0F)

    assert constraint.matches(3)
    assert constraint.matches(5)
    assert constraint.matches(7)
    assert constraint.matches(15)


def test_rejects_outside_mask():

    constraint = BitmaskConstraint(0x0F)

    assert not constraint.matches(16)
    assert not constraint.matches(31)
    assert not constraint.matches(255)


def test_rejects_non_integer():

    constraint = BitmaskConstraint(0x0F)

    assert not constraint.matches(1.0)
    assert not constraint.matches("1")
    assert not constraint.matches(None)


def test_negative_mask():

    with raises(ValueError):
        BitmaskConstraint(-1)