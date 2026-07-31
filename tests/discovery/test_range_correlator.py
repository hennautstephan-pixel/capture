from capture_recovery.discovery import (
    EnumConstraint,
    EnumCorrelator,
    PropertyObservation,
)


def make(value: int) -> PropertyObservation:
    return PropertyObservation(
        object_type="Fixture",
        offset=100,
        semantic_property="Mode",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def test_detect_enum():

    correlator = EnumCorrelator()

    observations = [
        make(0),
        make(1),
        make(2),
        make(0),
        make(1),
        make(2),
    ]

    candidate = correlator.analyse(observations)

    assert candidate is not None

    assert candidate.constraints == (
        EnumConstraint((0, 1, 2)),
    )


def test_reject_many_values():

    correlator = EnumCorrelator()

    observations = [
        make(i)
        for i in range(20)
    ]

    assert correlator.analyse(observations) is None