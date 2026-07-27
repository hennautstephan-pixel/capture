from capture_recovery.knowledge.default_knowledge import (
    create_default_registry,
)
from capture_recovery.knowledge.knowledge_engine import (
    KnowledgeEngine,
)
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def make_field(
    name,
    datatype,
    value,
    offset=0,
):
    return Field(
        name=name,
        offset=offset,
        length=4,
        datatype=datatype,
        value=value,
    )


def create_fixture_structure():

    structure = Structure(
        name="Fixture",
        offset=0,
        length=100,
    )

    structure.add(
        make_field(
            "name",
            DataType.STRING,
            "Mac Aura",
        )
    )

    structure.add(
        make_field(
            "universe",
            DataType.UINT16,
            1,
        )
    )

    structure.add(
        make_field(
            "address",
            DataType.UINT16,
            10,
        )
    )

    return structure


def create_universe_structure():

    structure = Structure(
        name="Universe",
        offset=100,
        length=50,
    )

    structure.add(
        make_field(
            "name",
            DataType.STRING,
            "Universe 1",
        )
    )

    structure.add(
        make_field(
            "universe",
            DataType.UINT16,
            1,
        )
    )

    return structure


def create_cue_structure():

    structure = Structure(
        name="Cue",
        offset=150,
        length=50,
    )

    structure.add(
        make_field(
            "name",
            DataType.STRING,
            "Intro",
        )
    )

    structure.add(
        make_field(
            "cue_number",
            DataType.UINT16,
            1,
        )
    )

    return structure


def test_knowledge_engine_decodes_multiple_objects():

    registry = create_default_registry()

    engine = KnowledgeEngine(
        registry,
    )

    objects = engine.infer(
        [
            create_fixture_structure(),
            create_universe_structure(),
            create_cue_structure(),
        ]
    )

    types = {
        obj.object_type
        for obj in objects
    }

    assert types == {
        "Fixture",
        "Universe",
        "Cue",
    }


def test_knowledge_engine_object_count():

    registry = create_default_registry()

    engine = KnowledgeEngine(
        registry,
    )

    objects = engine.infer(
        [
            create_fixture_structure(),
            create_universe_structure(),
            create_cue_structure(),
        ]
    )

    assert len(objects) == 3