from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.library import (
    FixtureDefinition,
    FixtureLibrary,
    FixtureResolver,
)


def create_library():

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

    return library


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


def test_resolve_known_fixture():

    resolver = FixtureResolver(
        create_library(),
    )

    definition = resolver.resolve(
        create_fixture(),
    )

    assert definition is not None

    assert definition.manufacturer == "Martin"

    assert definition.model == "MAC Aura"


def test_resolve_unknown_fixture():

    resolver = FixtureResolver(
        create_library(),
    )

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={
            "manufacturer": "Unknown",
            "model": "Nothing",
        },
    )

    result = resolver.resolve(
        fixture,
    )

    assert result is None


def test_reject_non_fixture_object():

    resolver = FixtureResolver(
        create_library(),
    )

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert resolver.resolve(
        universe,
    ) is None


def test_can_resolve():

    resolver = FixtureResolver(
        create_library(),
    )

    assert resolver.can_resolve(
        create_fixture(),
    ) is True


def test_enrich_fixture():

    resolver = FixtureResolver(
        create_library(),
    )

    result = resolver.enrich(
        create_fixture(),
    )

    assert result["library_manufacturer"] == "Martin"

    assert result["library_model"] == "MAC Aura"

    assert "dimmer" in result["library_channels"]

    assert result["library_geometry"]["beam_angle"] == 40


def test_enrich_unknown_fixture():

    resolver = FixtureResolver(
        create_library(),
    )

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={
            "manufacturer": "X",
            "model": "Y",
        },
    )

    result = resolver.enrich(
        fixture,
    )

    assert result["manufacturer"] == "X"

    assert "library_model" not in result