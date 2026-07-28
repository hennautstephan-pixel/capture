from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProject,
    FixtureMount,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_mounted_fixture():

    return SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={
            "manufacturer": "Martin",

            "model": "MAC Aura",

            "universe": 1,

            "address": 10,

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


def test_fixture_builder_adds_mount():

    builder = CaptureFixtureBuilder()

    result = builder.build(
        create_mounted_fixture(),
    )

    assert result.mount.structure_id == (
        "Face Truss"
    )

    assert result.mount.offset_x == 1.0

    assert result.mount.offset_z == -0.2


def test_fixture_mount_rotation():

    builder = CaptureFixtureBuilder()

    result = builder.build(
        create_mounted_fixture(),
    )

    assert result.mount.rotation == (
        0.0,
        180.0,
        0.0,
    )


def test_fixture_mount_default():

    fixture = SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={},
    )

    builder = CaptureFixtureBuilder()

    result = builder.build(
        fixture,
    )

    assert result.mount.structure_id is None

    assert result.mount.offset_x == 0.0


def test_mount_json_export():

    project = CaptureProject(
        name="Mount Test",
    )

    fixture = CaptureFixtureBuilder().build(
        create_mounted_fixture(),
    )

    project.add_fixture(
        fixture,
    )

    serializer = CaptureJsonSerializer()

    data = serializer.serialize(
        project,
    )

    assert data["fixtures"][0]["mount"] == {
        "structure_id": "Face Truss",

        "offset_x": 1.0,

        "offset_y": 0.0,

        "offset_z": -0.2,

        "rotation": [
            0.0,
            180.0,
            0.0,
        ],

        "properties": {
            "manufacturer": "Martin",

            "model": "MAC Aura",

            "universe": 1,

            "address": 10,

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
    }


def test_mount_json_import():

    project = CaptureProject(
        name="Mount Test",
    )

    fixture = CaptureFixtureBuilder().build(
        create_mounted_fixture(),
    )

    project.add_fixture(
        fixture,
    )

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    restored = loader.from_dict(
        serializer.serialize(
            project,
        )
    )

    result = restored.fixtures[0]

    assert result.mount.structure_id == (
        "Face Truss"
    )

    assert result.mount.offset_z == -0.2


def test_mount_type():

    fixture = CaptureFixtureBuilder().build(
        create_mounted_fixture(),
    )

    assert isinstance(
        fixture.mount,
        FixtureMount,
    )