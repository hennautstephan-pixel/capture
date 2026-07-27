from capture_recovery.inference import (
    InferenceEngine,
    InferenceResult,
    InferenceRule,
)
from capture_recovery.structures import Structure


class DummyRule(InferenceRule):

    @property
    def name(self):

        return "Dummy"

    def match(
        self,
        structure,
    ):

        return InferenceResult(
            matched=True,
            structure_name="Dummy",
            confidence=0.5,
        )


def test_engine():

    engine = InferenceEngine()

    engine.add_rule(DummyRule())

    result = engine.infer(

        Structure(
            "Unknown",
            0,
            10,
        )

    )

    assert result.matched

    assert result.structure_name == "Dummy"

    assert result.confidence == 0.5


def test_empty():

    engine = InferenceEngine()

    result = engine.infer(

        Structure(
            "Unknown",
            0,
            10,
        )

    )

    assert not result.matched