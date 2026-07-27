from capture_recovery.formats import (
    UniverseBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_universe():

    return SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={
            "universe": 1,
            "protocol": "sACN",
            "priority": 100,
            "ip_address": "2.0.0.1",
            "port": 5568,
        },
    )


def test_build_universe():

    builder = UniverseBuilder()

    result = builder.build(
        create_universe(),
    )

    assert result.name == "Universe 1"

    assert result.universe == 1


def test_build_preserves_protocol():

    builder = UniverseBuilder()

    result = builder.build(
        create_universe(),
    )

    assert result.protocol == "sACN"


def test_build_preserves_network_data():

    builder = UniverseBuilder()

    result = builder.build(
        create_universe(),
    )

    assert result.properties[
        "ip_address"
    ] == "2.0.0.1"

    assert result.properties[
        "port"
    ] == 5568


def test_build_preserves_priority():

    builder = UniverseBuilder()

    result = builder.build(
        create_universe(),
    )

    assert result.properties[
        "priority"
    ] == 100


def test_can_build_universe():

    builder = UniverseBuilder()

    assert builder.can_build(
        create_universe(),
    ) is True


def test_cannot_build_non_universe():

    builder = UniverseBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={},
    )

    assert builder.can_build(
        fixture,
    ) is False


def test_build_empty_universe():

    builder = UniverseBuilder()

    universe = SemanticObject(
        object_type="Universe",
        identifier="Unknown",
        properties={},
    )

    result = builder.build(
        universe,
    )

    assert result.universe == 0

    assert result.name == "Unknown"