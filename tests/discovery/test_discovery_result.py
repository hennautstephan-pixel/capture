from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.discovery import (
    DiscoveryResult,
    PropertyCandidate,
)


def make_candidate() -> PropertyCandidate:

    return PropertyCandidate(
        object_type="Fixture",
        property_name="Position.X",
        offset=0x184,
        value_type="float32",
        confidence=0.98,
        observations=12,
    )


def test_empty_result():

    result = DiscoveryResult()

    assert result.candidates == ()
    assert result.analysed_diffs == 0
    assert result.discovered_properties == 0
    assert result.is_empty is True
    assert result.has_candidates is False


def test_result_with_candidate():

    candidate = make_candidate()

    result = DiscoveryResult(
        candidates=(candidate,),
        analysed_diffs=42,
    )

    assert result.candidates == (candidate,)
    assert result.analysed_diffs == 42
    assert result.discovered_properties == 1
    assert result.is_empty is False
    assert result.has_candidates is True


def test_result_with_multiple_candidates():

    candidate1 = make_candidate()

    candidate2 = PropertyCandidate(
        object_type="Fixture",
        property_name="Rotation.Z",
        offset=0x1B4,
        value_type="float32",
        confidence=0.99,
        observations=8,
    )

    result = DiscoveryResult(
        candidates=(candidate1, candidate2),
        analysed_diffs=80,
    )

    assert result.discovered_properties == 2
    assert result.has_candidates is True
    assert result.is_empty is False


def test_result_is_immutable():

    result = DiscoveryResult()

    with pytest.raises(FrozenInstanceError):
        result.analysed_diffs = 1


def test_equal_results():

    candidate = make_candidate()

    result1 = DiscoveryResult(
        candidates=(candidate,),
        analysed_diffs=15,
    )

    result2 = DiscoveryResult(
        candidates=(candidate,),
        analysed_diffs=15,
    )

    assert result1 == result2
    assert hash(result1) == hash(result2)


def test_different_results():

    candidate = make_candidate()

    result1 = DiscoveryResult(
        candidates=(candidate,),
        analysed_diffs=15,
    )

    result2 = DiscoveryResult(
        candidates=(candidate,),
        analysed_diffs=16,
    )

    assert result1 != result2