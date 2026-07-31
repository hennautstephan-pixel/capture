from pytest import raises

from capture_recovery.discovery import StepConstraint


def test_name():

    constraint = StepConstraint(5)

    assert constraint.name == "StepConstraint"


def test_matches():

    constraint = StepConstraint(5)

    assert constraint.matches(0)
    assert constraint.matches(5)
    assert constraint.matches(10)
    assert constraint.matches(25)


def test_rejects():

    constraint = StepConstraint(5)

    assert not constraint.matches(3)
    assert not constraint.matches(17)


def test_invalid_step():

    with raises(ValueError):
        StepConstraint(0)

    with raises(ValueError):
        StepConstraint(-1)