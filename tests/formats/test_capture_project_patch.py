from capture_recovery.formats import (
    CaptureProjectBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.models.project import (
    Project,
)


def test_project_builder_creates_patch():

    project = Project(
        name="Patch Test",
    )

    project.add(
        SemanticObject(
            object_type="Fixture",
            identifier="MAC Aura",
            properties={
                "universe": 1,
                "address": 10,
                "mode": "Standard",
            },
        )
    )

    builder = CaptureProjectBuilder()

    result = builder.build(
        project,
    )

    assert len(
        result.patch
    ) == 1

    entry = result.patch.entries[0]

    assert entry.fixture == "MAC Aura"
    assert entry.universe == 1
    assert entry.address == 10