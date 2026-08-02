import pytest

from capture_recovery.reconstruction import ReconstructionCandidate


def test_candidate_creation():
    candidate = ReconstructionCandidate(
        score=0.75,
        heuristic="Dummy",
    )

    assert candidate.score == 0.75
    assert candidate.heuristic == "Dummy"


def test_confidence_alias():
    candidate = ReconstructionCandidate(
        score=0.42,
        heuristic="Dummy",
    )

    assert candidate.confidence == 0.42


def test_empty_candidate():
    candidate = ReconstructionCandidate.empty()

    assert candidate.score == 0.0
    assert candidate.is_empty


def test_invalid_score_low():
    with pytest.raises(ValueError):
        ReconstructionCandidate(
            score=-0.1,
            heuristic="Dummy",
        )


def test_invalid_score_high():
    with pytest.raises(ValueError):
        ReconstructionCandidate(
            score=1.5,
            heuristic="Dummy",
        )


def test_to_dict():
    candidate = ReconstructionCandidate(
        score=0.8,
        heuristic="Dummy",
        modifications={"offset": 12},
    )

    d = candidate.to_dict()

    assert d["score"] == 0.8
    assert d["heuristic"] == "Dummy"
    assert d["modifications"]["offset"] == 12