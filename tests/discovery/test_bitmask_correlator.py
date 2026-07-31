from capture_recovery.discovery import (
    BitmaskConstraint,
    BitmaskCorrelator,
    PropertyObservation,
)


def make(value: int) -> PropertyObservation:
    return PropertyObservation(
        object_type="Fixture",
        offset=100,
        semantic_property="Flags",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def test_priority():

    correlator = BitmaskCorrelator()

    assert correlator.priority == 30


def test_detect_bitmask():

    correlator = BitmaskCorrelator()

    observations = [
        make(0),
        make(1),
        make(2),
        make(4),
        make(8),
        make(3),
        make(5),
        make(7),
    ]

    candidate = correlator.analyse(observations)

    assert candidate is not None

    assert candidate.constraints == (
        BitmaskConstraint(0x0F),
    )


def test_detect_larger_mask():

    correlator = BitmaskCorrelator()

    observations = [
        make(0),
        make(1),
        make(2),
        make(4),
        make(8),
        make(16),
    ]

    candidate = correlator.analyse(observations)

    assert candidate is not None

    assert candidate.constraints == (
        BitmaskConstraint(0x1F),
    )


def test_reject_single_value():

    correlator = BitmaskCorrelator()

    observations = [
        make(4),
        make(4),
        make(4),
        make(4),
        make(4),
    ]

    assert correlator.analyse(observations) is None


def test_reject_zero_only():

    correlator = BitmaskCorrelator()

    observations = [
        make(0),
        make(0),
        make(0),
        make(0),
        make(0),
    ]

    assert correlator.analyse(observations) is None


def test_reject_negative():

    correlator = BitmaskCorrelator()

    observations = [
        make(-1),
        make(1),
        make(2),
        make(4),
        make(8),
    ]

    assert correlator.analyse(observations) is None