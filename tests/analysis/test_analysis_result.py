from capture_recovery.analysis import AnalysisResult
from capture_recovery.discovery import (
    PropertyCandidate,
    ValueType,
)


def test_defaults():

    result = AnalysisResult(
        filename="project.c2p",
        file_size=100,
        object_count=10,
        property_count=20,
        candidate_count=5,
        average_confidence=0.90,
        minimum_confidence=0.80,
        maximum_confidence=1.00,
        unknown_objects=2,
        unknown_signatures=1,
        conflict_count=0,
        duration_seconds=0.25,
    )

    assert result.filename == "project.c2p"
    assert result.file_size == 100
    assert result.object_count == 10
    assert result.property_count == 20
    assert result.candidate_count == 5
    assert result.average_confidence == 0.90
    assert result.minimum_confidence == 0.80
    assert result.maximum_confidence == 1.00
    assert result.unknown_objects == 2
    assert result.unknown_signatures == 1
    assert result.conflict_count == 0
    assert result.duration_seconds == 0.25
    assert result.candidates == ()


def test_recovered_objects():

    result = AnalysisResult(
        filename="project.c2p",
        file_size=0,
        object_count=100,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        unknown_objects=8,
        unknown_signatures=0,
        conflict_count=0,
        duration_seconds=0.0,
    )

    assert result.recovered_objects == 92


def test_recovery_rate():

    result = AnalysisResult(
        filename="project.c2p",
        file_size=0,
        object_count=100,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        unknown_objects=25,
        unknown_signatures=0,
        conflict_count=0,
        duration_seconds=0.0,
    )

    assert result.recovery_rate == 0.75


def test_zero_objects():

    result = AnalysisResult(
        filename="project.c2p",
        file_size=0,
        object_count=0,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        unknown_objects=0,
        unknown_signatures=0,
        conflict_count=0,
        duration_seconds=0.0,
    )

    assert result.recovery_rate == 0.0
    assert result.recovered_objects == 0


def test_candidates():

    candidate = PropertyCandidate(
        object_type="Fixture",
        property_name="Intensity",
        offset=123,
        value_type=ValueType.UINT8,
        confidence=0.95,
        observations=8,
    )

    result = AnalysisResult(
        filename="project.c2p",
        file_size=0,
        object_count=1,
        property_count=1,
        candidate_count=1,
        average_confidence=0.95,
        minimum_confidence=0.95,
        maximum_confidence=0.95,
        unknown_objects=0,
        unknown_signatures=0,
        conflict_count=0,
        duration_seconds=0.1,
        candidates=(candidate,),
    )

    assert len(result.candidates) == 1
    assert result.candidates[0] == candidate


def test_analysed():

    result = AnalysisResult(
        filename="project.c2p",
        file_size=0,
        object_count=0,
        property_count=0,
        candidate_count=0,
        average_confidence=0.0,
        minimum_confidence=0.0,
        maximum_confidence=0.0,
        unknown_objects=0,
        unknown_signatures=0,
        conflict_count=0,
        duration_seconds=0.0,
    )

    assert result.analysed