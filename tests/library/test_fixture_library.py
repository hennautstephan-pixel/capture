from capture_recovery.library.fixture_definition import (
    FixtureDefinition,
)
from capture_recovery.library.fixture_library import (
    FixtureLibrary,
)


def create_fixture():

    return FixtureDefinition(
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
    )


def test_register_fixture():

    library = FixtureLibrary()

    library.register(
        create_fixture(),
    )

    assert len(library) == 1


def test_find_fixture():

    library = FixtureLibrary()

    library.register(
        create_fixture(),
    )

    fixture = library.find(
        "Martin",
        "MAC Aura",
    )

    assert fixture is not None

    assert fixture.manufacturer == "Martin"


def test_fixture_channels():

    fixture = create_fixture()

    assert fixture.channel(
        "dimmer",
    ) == 1


def test_fixture_mode():

    fixture = create_fixture()

    assert fixture.has_mode(
        "Standard",
    )