from capture_recovery.formats import (
    FixtureGeometryBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "position": (
                3.5,
                2.0,
                6.0,
            ),
            "rotation": (
                180.0,
                45.0,
                0.0,
            ),
            "scale": (
                1.0,
                1.0,
                1.0,
            ),
            "height": 6.0,
            "focus_point": "Centre plateau",
        },
    )


def test_build_geometry():

    builder = FixtureGeometryBuilder()

    geometry = builder.build(
        create_fixture(),
    )

    assert geometry.position == (
        3.5,
        2.0,
        6.0,
    )

    assert geometry.rotation == (
        180.0,
        45.0,
        0.0,
    )

    assert geometry.height == 6.0


def test_build_scale():

    builder = FixtureGeometryBuilder()

    geometry = builder.build(
        create_fixture(),
    )

    assert geometry.scale == (
        1.0,
        1.0,
        1.0,
    )


def test_build_focus_point():

    builder = FixtureGeometryBuilder()

    geometry = builder.build(
        create_fixture(),
    )

    assert geometry.focus_point == (
        "Centre plateau"
    )


def test_build_default_values():

    builder = FixtureGeometryBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={},
    )

    geometry = builder.build(
        fixture,
    )

    assert geometry.position == (
        0.0,
        0.0,
        0.0,
    )

    assert geometry.rotation == (
        0.0,
        0.0,
        0.0,
    )

    assert geometry.scale == (
        1.0,
        1.0,
        1.0,
    )


def test_build_rejects_non_fixture():

    builder = FixtureGeometryBuilder()

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert builder.can_build(
        universe,
    ) is False


def test_build_accepts_fixture():

    builder = FixtureGeometryBuilder()

    assert builder.can_build(
        create_fixture(),
    ) is True


def test_build_metadata():

    builder = FixtureGeometryBuilder()

    geometry = builder.build(
        create_fixture(),
    )

    assert geometry.metadata["source"] == (
        "SemanticObject"
    )

    assert geometry.metadata["identifier"] == (
        "MAC Aura"
    )