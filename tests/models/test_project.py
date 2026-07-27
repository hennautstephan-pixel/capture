from capture_recovery.models.project import Project
from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="Mac Aura",
        properties={
            "manufacturer": "Martin",
            "model": "MAC Aura",
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


def test_project_add():

    project = Project()

    fixture = create_fixture()

    project.add(
        fixture,
    )

    assert len(project) == 1

    assert project.objects[0] == fixture


def test_project_grouping():

    project = Project()

    project.extend(
        [
            create_fixture(),
            create_universe(),
            create_cue(),
        ]
    )

    assert len(project.fixtures) == 1

    assert len(project.universes) == 1

    assert len(project.cues) == 1


def test_project_find():

    project = Project()

    project.extend(
        [
            create_fixture(),
            create_universe(),
            create_cue(),
        ]
    )

    result = project.find(
        "Fixture",
        "Mac Aura",
    )

    assert result is not None

    assert result.object_type == "Fixture"

    assert result.identifier == "Mac Aura"


def test_project_count():

    project = Project()

    project.extend(
        [
            create_fixture(),
            create_fixture(),
            create_universe(),
        ]
    )

    assert project.count() == 3

    assert project.count(
        "Fixture",
    ) == 2

    assert project.count(
        "Universe",
    ) == 1


def test_project_iteration():

    project = Project()

    project.extend(
        [
            create_fixture(),
            create_cue(),
        ]
    )

    objects = list(project)

    assert len(objects) == 2

    assert objects[0].object_type == "Fixture"