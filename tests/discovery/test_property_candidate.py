from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.discovery import PropertyCandidate


def test_create_property_candidate():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    assert candidate.object_type == "Fixture"
    assert candidate.property_name == "Position.X"
    assert candidate.offset == 0x184
    assert candidate.value_type == "float32"
    assert candidate.confidence == 0.98
    assert candidate.observations == 12


def test_confidence_percent():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.975,
        observations=20,
    )

    assert candidate.confidence_percent == 97.5


def test_is_high_confidence_true():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.95,
        observations=10,
    )

    assert candidate.is_high_confidence is True


def test_is_high_confidence_false():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.94,
        observations=10,
    )

    assert candidate.is_high_confidence is False


def test_identifier():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Rotation.Z",
        offset=0x1B4,
        value_type="float32",
        confidence=0.99,
        observations=8,
    )

    assert (
        candidate.identifier
        == "Fixture:Rotation.Z:0x1B4"
    )


def test_candidate_is_immutable():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    with pytest.raises(FrozenInstanceError):
        candidate.confidence = 0.5


def test_equal_candidates():

    candidate1 = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    candidate2 = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    assert candidate1 == candidate2
    assert hash(candidate1) == hash(candidate2)


def test_different_candidates():

    candidate1 = PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    candidate2 = PropertyCandidate(
        object_type="Fixture",
        property_name="Rotation.Z",
        offset=0x1B4,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )

    assert candidate1 != candidate2