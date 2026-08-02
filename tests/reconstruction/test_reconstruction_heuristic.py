from capture_recovery.reconstruction import (
    NoOpReconstructionHeuristic,
    ReconstructionContext,
)


def test_noop_returns_empty():
    heuristic = NoOpReconstructionHeuristic()

    context = ReconstructionContext(
        data=b"",
    )

    candidates = list(
        heuristic.reconstruct(context)
    )

    assert candidates == []


def test_supports():
    heuristic = NoOpReconstructionHeuristic()

    context = ReconstructionContext(
        data=b"",
    )

    assert heuristic.supports(context)