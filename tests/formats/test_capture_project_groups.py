from capture_recovery.formats import (
    CaptureProjectBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.models.project import (
    Project,
)


def create_group():

    return SemanticObject(
        object_type="Group",
        identifier="Face",
        properties={
            "fixtures": [
                "MAC Aura 1",
                "MAC Aura 2",
            ],
        },
    )


def create_project():

    project = Project(
        name="Group Test",
    )

    project.add(
        create_group(),
    )

    return project


def test_project_builder_creates_groups():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.groups,
    ) == 1


def test_project_builder_preserves_group_name():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    group = result.groups[0]

    assert group.name == "Face"


def test_project_builder_preserves_group_fixtures():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    group = result.groups[0]

    assert group.fixtures == [
        "MAC Aura 1",
        "MAC Aura 2",
    ]


def test_project_builder_ignores_non_group_objects():

    project = Project(
        name="No Group",
    )

    project.add(
        SemanticObject(
            object_type="Fixture",
            identifier="MAC Aura",
            properties={},
        )
    )

    builder = CaptureProjectBuilder()

    result = builder.build(
        project,
    )

    assert len(
        result.groups,
    ) == 0