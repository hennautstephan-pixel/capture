from capture_recovery.discovery import (
    IntegerCorrelator,
    PropertyObservation,
    ValueType,
)


def make_observation(value):

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Mode",
        binary_before=value,
        binary_after=value,
        semantic_before=value,
        semantic_after=value,
    )


def test_empty_observations():

    correlator = IntegerCorrelator()

    assert correlator.analyse(()) is None


def test_single_integer():

    correlator = IntegerCorrelator()

    candidate = correlator.analyse(
        (
            make_observation(42),
        )
    )

    assert candidate is not None
    assert candidate.value_type is ValueType.INT32


def test_multiple_integers():

    correlator = IntegerCorrelator()

    candidate = correlator.analyse(
        (
            make_observation(1),
            make_observation(2),
            make_observation(3),
        )
    )

    assert candidate is not None
    assert candidate.value_type is ValueType.INT32


def test_rejects_booleans():

    correlator = IntegerCorrelator()

    assert correlator.analyse(
        (
            make_observation(True),
            make_observation(False),
        )
    ) is None


def test_rejects_floats():

    correlator = IntegerCorrelator()

    assert correlator.analyse(
        (
            make_observation(1.0),
            make_observation(2.0),
        )
    ) is None


def test_rejects_strings():

    correlator = IntegerCorrelator()

    assert correlator.analyse(
        (
            make_observation("A"),
            make_observation("B"),
        )
    ) is None


def test_priority():

    correlator = IntegerCorrelator()

    assert correlator.priority == 20