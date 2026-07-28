from capture_recovery.formats import (
    FocusBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "focus_point": {
                "x": 4.0,
                "y": 5.0,
                "z": 1.5,
            },
        },
    )


def test_build_focus_point():

    builder = FocusBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert result.x == 4.0

    assert result.y == 5.0

    assert result.z == 1.5


def test_build_focus_tuple():

    builder = FocusBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "focus_point": (
                1.0,
                2.0,
                3.0,
            ),
        },
    )

    result = builder.build(
        fixture,
    )

    assert result.x == 1.0

    assert result.y == 2.0

    assert result.z == 3.0


def test_default_focus_point():

    builder = FocusBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Empty",
        properties={},
    )

    result = builder.build(
        fixture,
    )

    assert result.x == 0.0

    assert result.y == 0.0

    assert result.z == 0.0


def test_can_build_fixture():

    builder = FocusBuilder()

    assert builder.can_build(
        create_fixture(),
    )


def test_cannot_build_universe():

    builder = FocusBuilder()

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert not builder.can_build(
        universe,
    )