from capture_recovery.builders.project_builder import (
    ProjectBuilder,
)
from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)
from capture_recovery.models.project import Project


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="Mac Aura",
        properties={
            "manufacturer": "Martin",
        },
    )


def create_universe():

    return SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={
            "universe": 1,
        },
    )


def create_cue():

    return SemanticObject(
        object_type="Cue",
        identifier="Intro",
        properties={
            "cue_number": 1,
        },
    )


def test_build_project_from_objects():

    builder = ProjectBuilder()

    objects = (
        create_fixture(),
        create_universe(),
        create_cue(),
    )

    project = builder.build(
        objects,
    )

    assert isinstance(
        project,
        Project,
    )

    assert len(project) == 3


def test_build_project_groups_objects():

    builder = ProjectBuilder()

    project = builder.build(
        [
            create_fixture(),
            create_universe(),
            create_cue(),
        ]
    )

    assert len(project.fixtures) == 1

    assert len(project.universes) == 1

    assert len(project.cues) == 1


def test_custom_project_name():

    builder = ProjectBuilder(
        name="Recovered Capture",
    )

    project = builder.build(
        [],
    )

    assert project.name == "Recovered Capture"


def test_add_object_to_existing_project():

    builder = ProjectBuilder()

    project = Project()

    fixture = create_fixture()

    result = builder.add(
        project,
        fixture,
    )

    assert result is project

    assert len(project) == 1

    assert project.fixtures[0] == fixture


def test_builder_repr():

    builder = ProjectBuilder(
        name="Test",
    )

    assert "ProjectBuilder" in repr(
        builder,
    )