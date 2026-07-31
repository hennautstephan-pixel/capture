from capture_recovery.discovery import (
    PropertyObservation,
    ValueType,
    build_candidate,
    compute_confidence,
    validate_common_constraints,
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


def test_compute_confidence_empty():

    assert compute_confidence([]) == 0.0


def test_compute_confidence_single():

    confidence = compute_confidence(
        [
            make_observation(),
        ]
    )

    assert confidence == 1.0


def test_compute_confidence_partial():

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

    assert compute_confidence(observations) == 0.5


def test_validate_common_constraints_ok():

    assert validate_common_constraints(
        [
            make_observation(),
            make_observation(),
        ]
    )


def test_validate_common_constraints_empty():

    assert not validate_common_constraints([])


def test_validate_common_constraints_offset():

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

    assert not validate_common_constraints(observations)


def test_validate_common_constraints_property():

    observations = [
        make_observation(),
        PropertyObservation(
            object_type="Fixture",
            offset=0x184,
            semantic_property="Rotation.Z",
            binary_before=0.0,
            binary_after=1.0,
            semantic_before=0.0,
            semantic_after=1.0,
        ),
    ]

    assert not validate_common_constraints(observations)


def test_validate_common_constraints_object_type():

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

    assert not validate_common_constraints(observations)


def test_build_candidate():

    observations = [
        make_observation(),
        make_observation(),
    ]

    candidate = build_candidate(
        observations,
        value_type=ValueType.FLOAT32,
        confidence=1.0,
    )

    assert candidate.object_type == "Fixture"
    assert candidate.property_name == "Position.X"
    assert candidate.offset == 0x184
    assert candidate.value_type is ValueType.FLOAT32
    assert candidate.confidence == 1.0
    assert candidate.observations == 2