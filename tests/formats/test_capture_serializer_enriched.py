from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureSerializer,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library import (
    FixtureDefinition,
    FixtureLibrary,
    FixtureResolver,
)

from capture_recovery.models.project import Project


def test_serializer_enriches_fixture():

    library = FixtureLibrary()

    library.register(
        FixtureDefinition(
            manufacturer="Martin",
            model="MAC Aura",
            channels={
                "dimmer": 1,
            },
        )
    )

    builder = CaptureFixtureBuilder(
        FixtureResolver(
            library,
        )
    )

    project = Project(
        name="Test",
    )

    project.add(
        SemanticObject(
            object_type="Fixture",
            identifier="MAC Aura",
            properties={
                "manufacturer": "Martin",
                "model": "MAC Aura",
                "universe": 1,
                "address": 10,
            },
        )
    )

    result = CaptureSerializer(
        fixture_builder=builder,
    ).serialize(
        project,
    )

    fixture = result.fixtures[0]

    assert fixture.properties["channels"]["dimmer"] == 1