from capture_recovery.formats import (
    CaptureFixtureBuilder,
    CaptureProjectBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library import (
    FixtureDefinition,
    FixtureLibrary,
    FixtureResolver,
)

from capture_recovery.models.project import (
    Project,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "manufacturer": "Martin",
            "model": "MAC Aura",
            "mode": "Standard",
            "universe": 1,
            "address": 10,

            "position": (
                3.5,
                2.0,
                6.0,
            ),

            "rotation": (
                180.0,
                45.0,
                0.0,
            ),

            "height": 6.0,

            "focus_point": "Centre plateau",
        },
    )


def create_universe():

    return SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={
            "universe": 1,
            "protocol": "sACN",
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


def create_project():

    project = Project(
        name="Enriched Project",
    )

    project.add(
        create_fixture(),
    )

    project.add(
        create_universe(),
    )

    project.add(
        create_cue(),
    )

    return project


def create_builder():

    library = FixtureLibrary()

    library.register(
        FixtureDefinition(
            manufacturer="Martin",
            model="MAC Aura",
            modes=[
                "Standard",
            ],
            channels={
                "dimmer": 1,
                "pan": 2,
                "tilt": 3,
            },
            geometry={
                "beam_angle": 40,
                "zoom": 20,
            },
        )
    )

    resolver = FixtureResolver(
        library,
    )

    fixture_builder = CaptureFixtureBuilder(
        resolver,
    )

    return CaptureProjectBuilder(
        fixture_builder=fixture_builder,
    )


def test_enriched_project_builds_fixture():

    builder = create_builder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.fixtures
    ) == 1

    fixture = result.fixtures[0]

    assert fixture.properties[
        "channels"
    ]["dimmer"] == 1


def test_enriched_project_preserves_geometry():

    builder = create_builder()

    result = builder.build(
        create_project(),
    )

    fixture = result.fixtures[0]

    assert fixture.properties[
        "geometry"
    ]["beam_angle"] == 40


def test_enriched_project_preserves_placement():

    builder = create_builder()

    result = builder.build(
        create_project(),
    )

    fixture = result.fixtures[0]

    assert fixture.properties[
        "placement"
    ]["height"] == 6.0


def test_enriched_project_contains_universe_and_cue():

    builder = create_builder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.universes
    ) == 1

    assert len(
        result.cues
    ) == 1