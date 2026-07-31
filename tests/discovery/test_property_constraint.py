from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.discovery import PropertyConstraint


def test_name():

    constraint = PropertyConstraint()

    assert constraint.name == "PropertyConstraint"


def test_equality():

    assert PropertyConstraint() == PropertyConstraint()


def test_is_frozen():

    constraint = PropertyConstraint()

    with pytest.raises(FrozenInstanceError):
        constraint.test = 1


def test_slots():

    constraint = PropertyConstraint()

    assert not hasattr(constraint, "__dict__")