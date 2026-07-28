from capture_recovery.formats import (
    PatchBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_fixture(
    identifier="MAC Aura",
    address=10,
):

    return SemanticObject(
        object_type="Fixture",
        identifier=identifier,
        properties={
            "universe": 1,
            "address": address,
            "mode": "Standard",
            "channels": 20,
        },
    )


def test_build_patch_entry():

    builder = PatchBuilder()

    result = builder.build(
        [
            create_fixture(),
        ],
    )

    assert len(
        result.entries,
    ) == 1

    entry = result.entries[0]

    assert entry.fixture == "MAC Aura"
    assert entry.universe == 1
    assert entry.address == 10
    assert entry.mode == "Standard"
    assert entry.channels == 20


def test_build_multiple_fixtures():

    builder = PatchBuilder()

    result = builder.build(
        [
            create_fixture(
                "MAC Aura 1",
                10,
            ),
            create_fixture(
                "MAC Aura 2",
                30,
            ),
        ],
    )

    assert len(
        result.entries,
    ) == 2

    assert result.entries[0].address == 10

    assert result.entries[1].address == 30


def test_build_preserves_properties():

    builder = PatchBuilder()

    fixture = create_fixture()

    fixture.properties["custom"] = (
        "value"
    )

    result = builder.build(
        [
            fixture,
        ],
    )

    assert result.entries[0].properties[
        "custom"
    ] == "value"


def test_can_build_fixture():

    builder = PatchBuilder()

    assert builder.can_build(
        create_fixture(),
    ) is True


def test_cannot_build_universe():

    builder = PatchBuilder()

    universe = SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={},
    )

    assert builder.can_build(
        universe,
    ) is False


def test_build_defaults():

    builder = PatchBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="Unknown",
        properties={},
    )

    result = builder.build(
        [
            fixture,
        ],
    )

    entry = result.entries[0]

    assert entry.universe == 0
    assert entry.address == 0
    assert entry.mode is None
    assert entry.channels == 0