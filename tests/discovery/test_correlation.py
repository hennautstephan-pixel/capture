from capture_recovery.discovery import (
    Correlation,
    NumericCorrelator,
)


def test_numeric_correlator_implements_protocol():

    correlator = NumericCorrelator()

    assert isinstance(
        correlator,
        Correlation,
    )


def test_default_priority():

    correlator = NumericCorrelator()

    assert correlator.priority == 10


def test_priority_is_integer():

    correlator = NumericCorrelator()

    assert isinstance(
        correlator.priority,
        int,
    )


def test_priority_is_positive():

    correlator = NumericCorrelator()

    assert correlator.priority > 0