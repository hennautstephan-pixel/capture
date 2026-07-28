from capture_recovery.formats import (
    StructureBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_truss():

    return SemanticObject(
        object_type="Structure",

        identifier="Face Truss",

        properties={
            "type": "Truss",

            "position": (
                0.0,
                0.0,
                6.0,
            ),

            "rotation": (
                0.0,
                0.0,
                0.0,
            ),

            "length": 8.0,
        },
    )


def test_build_structure():

    builder = StructureBuilder()

    result = builder.build(
        create_truss(),
    )

    assert result.name == "Face Truss"

    assert result.structure_type == "Truss"

    assert result.length == 8.0


def test_structure_position():

    builder = StructureBuilder()

    result = builder.build(
        create_truss(),
    )

    assert result.position == (
        0.0,
        0.0,
        6.0,
    )


def test_can_build_structure():

    builder = StructureBuilder()

    assert builder.can_build(
        create_truss(),
    )


def test_cannot_build_fixture():

    builder = StructureBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={},
    )

    assert not builder.can_build(
        fixture,
)