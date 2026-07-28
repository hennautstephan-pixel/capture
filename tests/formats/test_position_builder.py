from capture_recovery.formats import (
    PositionBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "position": {
                "x": 3.5,
                "y": 2.0,
                "z": 6.0,
            },
            "rotation": {
                "pan": 180.0,
                "tilt": 45.0,
                "roll": 0.0,
            },
        },
    )


def test_build_position():

    builder = PositionBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert result.x == 3.5
    assert result.y == 2.0
    assert result.z == 6.0


def test_build_rotation():

    builder = PositionBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert result.pan == 180.0
    assert result.tilt == 45.0
    assert result.roll == 0.0


def test_position_defaults():

    builder = PositionBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={},
    )

    result = builder.build(
        fixture,
    )

    assert result.x == 0.0
    assert result.y == 0.0
    assert result.z == 0.0


def test_can_build_fixture():

    builder = PositionBuilder()

    assert builder.can_build(
        create_fixture(),
    )


def test_cannot_build_universe():

    builder = PositionBuilder()

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert not builder.can_build(
        universe,
    )