from capture_recovery.formats import (
    BindingBuilder,
    CaptureFixtureBuilder,
    CaptureProject,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture(
    name,
):

    return SemanticObject(
        object_type="Fixture",

        identifier=name,

        properties={
            "mount": {
                "structure_id": "Face Truss",
            },
        },
    )


def test_build_structure_binding():

    project = CaptureProject(
        name="Binding Test",
    )

    builder = CaptureFixtureBuilder()

    project.add_fixture(
        builder.build(
            create_fixture(
                "MAC Aura",
            )
        )
    )

    bindings = BindingBuilder().build(
        project,
    )

    assert len(
        bindings,
    ) == 1


def test_binding_contains_fixture():

    project = CaptureProject(
        name="Binding Test",
    )

    builder = CaptureFixtureBuilder()

    project.add_fixture(
        builder.build(
            create_fixture(
                "MAC Aura",
            )
        )
    )

    binding = (
        BindingBuilder()
        .build(project)[0]
    )

    assert (
        "MAC Aura"
        in binding.fixtures
    )


def test_unmounted_fixture_not_bound():

    fixture = SemanticObject(
        object_type="Fixture",

        identifier="Floor Fixture",

        properties={},
    )

    project = CaptureProject(
        name="Binding Test",
    )

    project.add_fixture(
        CaptureFixtureBuilder().build(
            fixture,
        )
    )

    bindings = BindingBuilder().build(
        project,
    )

    assert bindings == []