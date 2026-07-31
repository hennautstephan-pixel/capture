from capture_recovery.discovery import (
    PropertyDiscoveryEngine,
    PropertyObservation,
)


def make_observation(
    *,
    offset=0x184,
    property_name="Position.X",
):

    return PropertyObservation(
        object_type="Fixture",
        offset=offset,
        semantic_property=property_name,
        binary_before=0.0,
        binary_after=1.0,
        semantic_before=0.0,
        semantic_after=1.0,
    )


def test_empty():

    engine = PropertyDiscoveryEngine()

    result = engine.discover([])

    assert result.discovered_properties == 0
    assert result.analysed_diffs == 0


def test_single_group():

    engine = PropertyDiscoveryEngine()

    result = engine.discover(
        [
            make_observation(),
            make_observation(),
            make_observation(),
        ]
    )

    assert result.discovered_properties == 1
    assert result.analysed_diffs == 3

    candidate = result.candidates[0]

    assert candidate.property_name == "Position.X"
    assert candidate.offset == 0x184


def test_two_groups():

    engine = PropertyDiscoveryEngine()

    result = engine.discover(
        [
            make_observation(),
            make_observation(offset=0x200),
        ]
    )

    assert result.discovered_properties == 2


def test_same_offset_different_property():

    engine = PropertyDiscoveryEngine()

    result = engine.discover(
        [
            make_observation(),
            make_observation(property_name="Rotation.Z"),
        ]
    )

    assert result.discovered_properties == 2


def test_same_property_different_offset():

    engine = PropertyDiscoveryEngine()

    result = engine.discover(
        [
            make_observation(offset=0x184),
            make_observation(offset=0x1B4),
        ]
    )

    assert result.discovered_properties == 2


def test_result_is_deterministic():

    engine = PropertyDiscoveryEngine()

    observations = [
        make_observation(),
        make_observation(),
        make_observation(),
    ]

    result1 = engine.discover(observations)
    result2 = engine.discover(observations)

    assert result1 == result2