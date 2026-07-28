from capture_recovery.formats import (
    GroupBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_group():

    return SemanticObject(
        object_type="Group",
        identifier="Face",
        properties={
            "fixtures": [
                "MAC Aura 1",
                "MAC Aura 2",
            ],
        },
    )


def test_build_group():

    builder = GroupBuilder()

    result = builder.build(
        create_group(),
    )

    assert result.name == "Face"

    assert len(result) == 2


def test_group_contains_fixtures():

    builder = GroupBuilder()

    result = builder.build(
        create_group(),
    )

    assert (
        "MAC Aura 1"
        in result.fixtures
    )

    assert (
        "MAC Aura 2"
        in result.fixtures
    )


def test_group_preserves_properties():

    builder = GroupBuilder()

    result = builder.build(
        create_group(),
    )

    assert result.properties[
        "fixtures"
    ] == [
        "MAC Aura 1",
        "MAC Aura 2",
    ]


def test_can_build_group():

    builder = GroupBuilder()

    assert builder.can_build(
        create_group(),
    )


def test_cannot_build_fixture():

    builder = GroupBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={},
    )

    assert not builder.can_build(
        fixture,
    )