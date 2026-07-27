from __future__ import annotations

from capture_recovery.diff.models import StructureChange
from capture_recovery.diff.semantic_differ import SemanticDiffer
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def make_field(value=1) -> Field:
    return Field(
        name="Value",
        offset=0,
        length=4,
        datatype=DataType.INT32,
        value=value,
    )


def make_structure(
    *,
    name="Fixture",
    offset=0,
    length=16,
    confidence=1.0,
    fields=None,
):
    return Structure(
        name=name,
        offset=offset,
        length=length,
        confidence=confidence,
        fields=[] if fields is None else fields,
    )


def test_empty():
    differ = SemanticDiffer()

    result = differ.compare(())

    assert result == ()


def test_added_structure():
    differ = SemanticDiffer()

    after = make_structure(offset=100)

    result = differ.compare(
        (
            StructureChange(
                offset=100,
                structure_after=after,
                changed_fields=("added",),
            ),
        )
    )

    assert len(result) == 1

    change = result[0]

    assert change.offset == 100
    assert change.object_type == "Fixture"
    assert change.object_identifier == 100
    assert change.property_name == "structure"
    assert change.before is None
    assert change.after == "added"


def test_removed_structure():
    differ = SemanticDiffer()

    before = make_structure(offset=100)

    result = differ.compare(
        (
            StructureChange(
                offset=100,
                structure_before=before,
                changed_fields=("removed",),
            ),
        )
    )

    assert len(result) == 1

    change = result[0]

    assert change.before == "present"
    assert change.after is None


def test_name_change():
    differ = SemanticDiffer()

    before = make_structure(name="Fixture")
    after = make_structure(name="Spot")

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("name",),
            ),
        )
    )

    assert len(result) == 1

    change = result[0]

    assert change.property_name == "name"
    assert change.before == "Fixture"
    assert change.after == "Spot"


def test_length_change():
    differ = SemanticDiffer()

    before = make_structure(length=16)
    after = make_structure(length=32)

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("length",),
            ),
        )
    )

    assert result[0].before == 16
    assert result[0].after == 32


def test_confidence_change():
    differ = SemanticDiffer()

    before = make_structure(confidence=0.5)
    after = make_structure(confidence=1.0)

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("confidence",),
            ),
        )
    )

    assert result[0].before == 0.5
    assert result[0].after == 1.0


def test_fields_change():
    differ = SemanticDiffer()

    before = make_structure(fields=[make_field(1)])
    after = make_structure(fields=[make_field(2)])

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("fields",),
            ),
        )
    )

    assert len(result) == 1
    assert result[0].property_name == "fields"
    assert result[0].before == before.fields
    assert result[0].after == after.fields


def test_multiple_changes():
    differ = SemanticDiffer()

    before = make_structure(
        name="Old",
        length=16,
    )

    after = make_structure(
        name="New",
        length=32,
    )

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("name", "length"),
            ),
        )
    )

    assert len(result) == 2

    assert result[0].property_name == "name"
    assert result[1].property_name == "length"


def test_confidence_propagation():
    differ = SemanticDiffer()

    before = make_structure()
    after = make_structure(name="Spot")

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before,
                structure_after=after,
                changed_fields=("name",),
                confidence=0.82,
            ),
        )
    )

    assert result[0].confidence == 0.82


def test_result_is_tuple():
    differ = SemanticDiffer()

    result = differ.compare(())

    assert isinstance(result, tuple)


def test_multiple_structure_changes():
    differ = SemanticDiffer()

    before1 = make_structure(offset=0, name="A")
    after1 = make_structure(offset=0, name="B")

    before2 = make_structure(offset=100, length=16)
    after2 = make_structure(offset=100, length=32)

    result = differ.compare(
        (
            StructureChange(
                offset=0,
                structure_before=before1,
                structure_after=after1,
                changed_fields=("name",),
            ),
            StructureChange(
                offset=100,
                structure_before=before2,
                structure_after=after2,
                changed_fields=("length",),
            ),
        )
    )

    assert len(result) == 2

    assert result[0].offset == 0
    assert result[1].offset == 100