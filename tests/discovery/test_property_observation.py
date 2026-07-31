from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.discovery import PropertyObservation


def make_observation() -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=0.0,
        binary_after=1.0,
        semantic_before=0.0,
        semantic_after=1.0,
    )


def test_create_observation():

    observation = make_observation()

    assert observation.object_type == "Fixture"
    assert observation.offset == 0x184
    assert observation.semantic_property == "Position.X"
    assert observation.binary_before == 0.0
    assert observation.binary_after == 1.0
    assert observation.semantic_before == 0.0
    assert observation.semantic_after == 1.0


def test_identifier():

    observation = make_observation()

    assert (
        observation.identifier
        == "Fixture:Position.X:0x184"
    )


def test_binary_changed_true():

    observation = make_observation()

    assert observation.binary_changed is True


def test_binary_changed_false():

    observation = PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=5.0,
        binary_after=5.0,
        semantic_before=5.0,
        semantic_after=5.0,
    )

    assert observation.binary_changed is False


def test_semantic_changed_true():

    observation = make_observation()

    assert observation.semantic_changed is True


def test_semantic_changed_false():

    observation = PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=2.0,
        binary_after=2.0,
        semantic_before=2.0,
        semantic_after=2.0,
    )

    assert observation.semantic_changed is False


def test_consistent_when_both_change():

    observation = make_observation()

    assert observation.is_consistent is True


def test_consistent_when_nothing_changes():

    observation = PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=2.0,
        binary_after=2.0,
        semantic_before=2.0,
        semantic_after=2.0,
    )

    assert observation.is_consistent is True


def test_inconsistent_when_only_binary_changes():

    observation = PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=1.0,
        binary_after=2.0,
        semantic_before=1.0,
        semantic_after=1.0,
    )

    assert observation.is_consistent is False


def test_inconsistent_when_only_semantic_changes():

    observation = PropertyObservation(
        object_type="Fixture",
        offset=0x184,
        semantic_property="Position.X",
        binary_before=1.0,
        binary_after=1.0,
        semantic_before=1.0,
        semantic_after=2.0,
    )

    assert observation.is_consistent is False


def test_observation_is_immutable():

    observation = make_observation()

    with pytest.raises(FrozenInstanceError):
        observation.offset = 0


def test_equal_observations():

    observation1 = make_observation()
    observation2 = make_observation()

    assert observation1 == observation2
    assert hash(observation1) == hash(observation2)


def test_different_observations():

    observation1 = make_observation()

    observation2 = PropertyObservation(
        object_type="Fixture",
        offset=0x1B4,
        semantic_property="Rotation.Z",
        binary_before=0.0,
        binary_after=90.0,
        semantic_before=0.0,
        semantic_after=90.0,
    )

    assert observation1 != observation2