from capture_recovery.reconstruction import (
    ReconstructionCandidate,
    ReconstructionContext,
    ReconstructionHeuristic,
    ReconstructionRegistry,
)


class DummyHeuristic(ReconstructionHeuristic):

    def reconstruct(self, context):

        yield ReconstructionCandidate(
            score=0.8,
            heuristic="Dummy",
        )


class BetterHeuristic(ReconstructionHeuristic):

    def reconstruct(self, context):

        yield ReconstructionCandidate(
            score=0.95,
            heuristic="Better",
        )


def test_register():

    registry = ReconstructionRegistry()

    registry.register(
        DummyHeuristic()
    )

    assert len(registry) == 1


def test_best():

    registry = ReconstructionRegistry()

    registry.register(
        DummyHeuristic()
    )

    registry.register(
        BetterHeuristic()
    )

    candidate = registry.best(
        ReconstructionContext(data=b"")
    )

    assert candidate.heuristic == "Better"


def test_run_returns_sorted():

    registry = ReconstructionRegistry()

    registry.register(
        DummyHeuristic()
    )

    registry.register(
        BetterHeuristic()
    )

    candidates = registry.run(
        ReconstructionContext(data=b"")
    )

    assert len(candidates) == 2
    assert candidates[0].score > candidates[1].score


def test_clear():

    registry = ReconstructionRegistry()

    registry.register(
        DummyHeuristic()
    )

    registry.clear()

    assert len(registry) == 0