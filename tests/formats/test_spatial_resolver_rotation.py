from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureProject,
    SceneStructure,
    SpatialResolver,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_rotated_fixture():

    return SemanticObject(
        object_type="Fixture",

        identifier="MAC Aura",

        properties={
            "mount": {
                "structure_id": "Side Truss",

                "offset_x": 1.0,

                "offset_y": 0.0,

                "offset_z": 0.0,
            },
        },
    )


def test_structure_rotation_affects_fixture_position():

    project = CaptureProject(
        name="Rotation Test",
    )

    project.add_structure(
        SceneStructure(
            name="Side Truss",

            structure_type="Truss",

            position=(
                0.0,
                0.0,
                6.0,
            ),

            rotation=(
                0.0,
                90.0,
                0.0,
            ),
        )
    )

    fixture = CaptureFixtureBuilder().build(
        create_rotated_fixture(),
    )

    project.add_fixture(
        fixture,
    )

    result = SpatialResolver().resolve_fixture(
        fixture,
        project,
    )

    assert round(
        result.x,
        5,
    ) == 0.0

    assert round(
        result.z,
        5,
    ) == 5.0


def test_project_rotation_resolution():

    project = CaptureProject(
        name="Rotation Test",
    )

    fixture = CaptureFixtureBuilder().build(
        create_rotated_fixture(),
    )

    project.add_fixture(
        fixture,
    )

    result = SpatialResolver().resolve_project(
        project,
    )

    assert "MAC Aura" in result