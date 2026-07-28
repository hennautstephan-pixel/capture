from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProject,
    FocusPoint,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_focus_fixture():

    return SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={
            "manufacturer": "Martin",

            "model": "MAC Aura",

            "universe": 1,

            "address": 10,

            "position": {
                "x": 4.0,
                "y": 2.5,
                "z": 7.0,
                "pan": 180.0,
                "tilt": 45.0,
                "roll": 0.0,
            },

            "focus_point": {
                "x": 4.0,
                "y": 5.0,
                "z": 1.5,
            },
        },
    )


def test_fixture_builder_adds_focus_point():

    builder = CaptureFixtureBuilder()

    result = builder.build(
        create_focus_fixture(),
    )

    assert result.focus_point.x == 4.0

    assert result.focus_point.y == 5.0

    assert result.focus_point.z == 1.5


def test_fixture_focus_point_default():

    fixture = SemanticObject(
        object_type="Fixture",

        identifier="Empty",

        properties={},
    )

    builder = CaptureFixtureBuilder()

    result = builder.build(
        fixture,
    )

    assert result.focus_point.x == 0.0

    assert result.focus_point.y == 0.0

    assert result.focus_point.z == 0.0


def test_focus_point_json_export():

    project = CaptureProject(
        name="Focus Test",
    )

    fixture = CaptureFixtureBuilder().build(
        create_focus_fixture(),
    )

    project.add_fixture(
        fixture,
    )

    serializer = CaptureJsonSerializer()

    data = serializer.serialize(
        project,
    )

    assert data["fixtures"][0]["focus_point"] == {
        "x": 4.0,
        "y": 5.0,
        "z": 1.5,
    }


def test_focus_point_json_import():

    project = CaptureProject(
        name="Focus Test",
    )

    fixture = CaptureFixtureBuilder().build(
        create_focus_fixture(),
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

    assert result.focus_point.x == 4.0

    assert result.focus_point.y == 5.0

    assert result.focus_point.z == 1.5


def test_focus_point_type():

    fixture = CaptureFixtureBuilder().build(
        create_focus_fixture(),
    )

    assert isinstance(
        fixture.focus_point,
        FocusPoint,
    )