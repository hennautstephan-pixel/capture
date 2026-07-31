from capture_recovery.discovery import (
    PropertyObservation,
    StepConstraint,
    StepCorrelator,
)


def make(value: int) -> PropertyObservation:
    return PropertyObservation(
        object_type="Fixture",
        offset=100,
        semantic_property="Intensity",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def test_priority():

    assert StepCorrelator().priority == 25


def test_detect_step():

    observations = [
        make(0),
        make(5),
        make(10),
        make(15),
        make(20),
        make(25),
    ]

    candidate = StepCorrelator().analyse(observations)

    assert candidate is not None

    assert candidate.constraints == (
        StepConstraint(5),
    )


def test_detect_step10():

    observations = [
        make(0),
        make(10),
        make(20),
        make(30),
        make(40),
    ]

    candidate = StepCorrelator().analyse(observations)

    assert candidate.constraints == (
        StepConstraint(10),
    )


def test_reject_step1():

    observations = [
        make(0),
        make(1),
        make(2),
        make(3),
        make(4),
    ]

    assert StepCorrelator().analyse(observations) is None


def test_reject_single_value():

    observations = [make(5)] * 5

    assert StepCorrelator().analyse(observations) is None