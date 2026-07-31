from typing import Sequence

from capture_recovery.discovery import (
    Correlation,
    PropertyCandidate,
    PropertyObservation,
    ValueType,
)


class DummyCorrelator:

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:

        if not observations:
            return None

        return PropertyCandidate(
            object_type="Fixture",
            property_name="Position.X",
            offset=0x184,
            value_type=ValueType.FLOAT32,
            confidence=1.0,
            observations=len(observations),
        )


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


def test_dummy_correlator_implements_protocol():

    correlator: Correlation = DummyCorrelator()

    result = correlator.analyse(
        [make_observation()]
    )

    assert result is not None
    assert result.property_name == "Position.X"


def test_dummy_correlator_returns_none_for_empty_input():

    correlator: Correlation = DummyCorrelator()

    assert correlator.analyse([]) is None


def test_dummy_correlator_counts_observations():

    correlator: Correlation = DummyCorrelator()

    observations = [
        make_observation(),
        make_observation(),
        make_observation(),
    ]

    result = correlator.analyse(observations)

    assert result is not None
    assert result.observations == 3