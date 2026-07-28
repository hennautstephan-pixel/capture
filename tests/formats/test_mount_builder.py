from capture_recovery.formats import (
    MountBuilder,
    FixtureMount,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={
            "mount": {
                "structure_id": "Face Truss",

                "offset_x": 1.0,

                "offset_y": 0.0,

                "offset_z": -0.2,

                "rotation": (
                    0.0,
                    180.0,
                    0.0,
                ),
            },
        },
    )


def test_build_mount():

    builder = MountBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert result.structure_id == (
        "Face Truss"
    )

    assert result.offset_x == 1.0

    assert result.offset_z == -0.2


def test_mount_rotation():

    builder = MountBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert result.rotation == (
        0.0,
        180.0,
        0.0,
    )


def test_default_mount():

    fixture = SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={},
    )

    builder = MountBuilder()

    result = builder.build(
        fixture,
    )

    assert result.structure_id is None

    assert result.offset_x == 0.0


def test_can_build_fixture():

    builder = MountBuilder()

    assert builder.can_build(
        create_fixture(),
    )


def test_mount_type():

    builder = MountBuilder()

    result = builder.build(
        create_fixture(),
    )

    assert isinstance(
        result,
        FixtureMount,
    )