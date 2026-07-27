from capture_recovery.formats import (
    CaptureFixtureBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library import (
    FixtureDefinition,
    FixtureLibrary,
    FixtureResolver,
)


def create_resolver():

    library = FixtureLibrary()

    library.register(
        FixtureDefinition(
            manufacturer="Martin",
            model="MAC Aura",
            modes=[
                "Standard",
                "Extended",
            ],
            channels={
                "dimmer": 1,
                "pan": 2,
                "tilt": 3,
            },
            geometry={
                "beam_angle": 40,
            },
        )
    )

    return FixtureResolver(
        library,
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
        },
    )


def test_build_known_fixture():

    builder = CaptureFixtureBuilder(
        create_resolver(),
    )

    result = builder.build(
        create_fixture(),
    )

    assert result.name == "MAC Aura"

    assert result.universe == 1

    assert result.address == 10

    assert result.manufacturer == "Martin"

    assert result.model == "MAC Aura"


def test_build_injects_library_data():

    builder = CaptureFixtureBuilder(
        create_resolver(),
    )

    result = builder.build(
        create_fixture(),
    )

    assert "channels" in result.properties

    assert result.properties["channels"]["dimmer"] == 1

    assert result.properties["channels"]["pan"] == 2

    assert result.properties["geometry"]["beam_angle"] == 40


def test_build_unknown_fixture():

    builder = CaptureFixtureBuilder(
        create_resolver(),
    )

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={
            "manufacturer": "Unknown",
            "model": "Unknown",
            "universe": 2,
            "address": 20,
        },
    )

    result = builder.build(
        fixture,
    )

    assert result.name == "Unknown"

    assert result.universe == 2

    assert result.address == 20

    assert "channels" not in result.properties


def test_can_build_fixture():

    builder = CaptureFixtureBuilder(
        create_resolver(),
    )

    assert builder.can_build(
        create_fixture(),
    ) is True


def test_cannot_build_non_fixture():

    builder = CaptureFixtureBuilder(
        create_resolver(),
    )

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert builder.can_build(
        universe,
    ) is False