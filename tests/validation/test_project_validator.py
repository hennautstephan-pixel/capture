from capture_recovery.validation.project_validator import (
    ProjectValidator,
)
from capture_recovery.models.project import Project
from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def fixture(
    name,
    universe=1,
    address=10,
):
    return SemanticObject(
        object_type="Fixture",
        identifier=name,
        properties={
            "universe": universe,
            "address": address,
        },
    )


def test_valid_project():

    project = Project()

    project.add(
        fixture("Mac Aura"),
    )

    result = ProjectValidator().validate(
        project,
    )

    assert result.valid is True


def test_duplicate_fixture_address():

    project = Project()

    project.extend(
        [
            fixture("A"),
            fixture("B"),
        ]
    )

    result = ProjectValidator().validate(
        project,
    )

    assert result.valid is False

    assert len(result.errors) == 1


def test_invalid_address():

    project = Project()

    project.add(
        fixture(
            "Bad",
            address=600,
        )
    )

    result = ProjectValidator().validate(
        project,
    )

    assert result.valid is False