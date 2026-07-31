from capture_recovery.discovery import (
    NumericCorrelator,
    PropertyObservation,
    ValueType,
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


def test_empty():

    correlator = NumericCorrelator()

    assert correlator.analyse([]) is None


def test_single_observation():

    correlator = NumericCorrelator()

    result = correlator.analyse(
        [make_observation()]
    )

    assert result is not None
    assert result.object_type == "Fixture"
    assert result.property_name == "Position.X"
    assert result.offset == 0x184
    assert result.value_type is ValueType.FLOAT32
    assert result.confidence == 1.0
    assert result.observations == 1


def test_multiple_observations():

    correlator = NumericCorrelator()

    observations = [
        make_observation(),
        make_observation(),
        make_observation(),
    ]

    result = correlator.analyse(observations)

    assert result is not None
    assert result.confidence == 1.0
    assert result.observations == 3


def test_inconsistent_returns_none():

    correlator = NumericCorrelator()

    observations = [
        make_observation(),
        PropertyObservation(
            object_type="Fixture",
            offset=0x184,
            semantic_property="Position.X",
            binary_before=1.0,
            binary_after=2.0,
            semantic_before=1.0,
            semantic_after=1.0,
        ),
    ]

    assert correlator.analyse(observations) is None


def test_different_offsets():

    correlator = NumericCorrelator()

    observations = [
        make_observation(),
        PropertyObservation(
            object_type="Fixture",
            offset=0x200,
            semantic_property="Position.X",
            binary_before=0.0,
            binary_after=1.0,
            semantic_before=0.0,
            semantic_after=1.0,
        ),
    ]

    assert correlator.analyse(observations) is None


def test_different_property():

    correlator = NumericCorrelator()

    observations = [
        make_observation(),
        PropertyObservation(
            object_type="Fixture",
            offset=0x184,
            semantic_property="Rotation.Z",
            binary_before=0.0,
            binary_after=90.0,
            semantic_before=0.0,
            semantic_after=90.0,
        ),
    ]

    assert correlator.analyse(observations) is None


def test_different_object_type():

    correlator = NumericCorrelator()

    observations = [
        make_observation(),
        PropertyObservation(
            object_type="Universe",
            offset=0x184,
            semantic_property="Position.X",
            binary_before=0.0,
            binary_after=1.0,
            semantic_before=0.0,
            semantic_after=1.0,
        ),
    ]

    assert correlator.analyse(observations) is None