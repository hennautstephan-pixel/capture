from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureProject,
    SceneStructure,
    SpatialResolver,
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
            },
        },
    )


def test_resolve_fixture_world_position():

    project = CaptureProject(
        name="Spatial Test",
    )

    project.structures.append(
        SceneStructure(
            name="Face Truss",

            structure_type="Truss",

            position=(
                0.0,
                0.0,
                6.0,
            ),
        )
    )

    project.fixtures.append(
        CaptureFixtureBuilder().build(
            create_fixture(),
        )
    )

    result = SpatialResolver().resolve_fixture(
        project.fixtures[0],
        project,
    )

    assert result.x == 1.0

    assert result.y == 0.0

    assert result.z == 5.8


def test_resolve_unmounted_fixture():

    fixture = CaptureFixtureBuilder().build(
        SemanticObject(
            object_type="Fixture",

            identifier="Floor Light",

            properties={},
        )
    )

    project = CaptureProject(
        name="Spatial Test",
    )

    project.fixtures.append(
        fixture,
    )

    result = SpatialResolver().resolve_fixture(
        fixture,
        project,
    )

    assert result.x == 0.0

    assert result.z == 0.0


def test_resolve_project():

    project = CaptureProject(
        name="Spatial Test",
    )

    project.fixtures.append(
        CaptureFixtureBuilder().build(
            create_fixture(),
        )
    )

    result = SpatialResolver().resolve_project(
        project,
    )

    assert "MAC Aura" in result