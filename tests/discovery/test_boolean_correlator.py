from capture_recovery.discovery import (
    BooleanCorrelator,
    PropertyObservation,
    ValueType,
)


def make_observation() -> PropertyObservation:

    return PropertyObservation(
        object_type="Fixture",
        offset=0x100,
        semantic_property="Visible",
        binary_before=0,
        binary_after=1,
        semantic_before=False,
        semantic_after=True,
    )


def test_empty():

    correlator = BooleanCorrelator()

    assert correlator.analyse([]) is None


def test_single_observation():

    correlator = BooleanCorrelator()

    result = correlator.analyse(
        [make_observation()]
    )

    assert result is not None
    assert result.object_type == "Fixture"
    assert result.property_name == "Visible"
    assert result.offset == 0x100
    assert result.value_type is ValueType.BOOL
    assert result.confidence == 1.0
    assert result.observations == 1


def test_multiple_observations():

    correlator = BooleanCorrelator()

    result = correlator.analyse(
        [
            make_observation(),
            make_observation(),
            make_observation(),
        ]
    )

    assert result is not None
    assert result.confidence == 1.0
    assert result.observations == 3


def test_non_boolean_returns_none():

    correlator = BooleanCorrelator()

    observations = [
        PropertyObservation(
            object_type="Fixture",
            offset=0x100,
            semantic_property="Visible",
            binary_before=0,
            binary_after=1,
            semantic_before=0,
            semantic_after=1,
        ),
    ]

    assert correlator.analyse(observations) is None


def test_priority():

    correlator = BooleanCorrelator()

    assert correlator.priority == 100