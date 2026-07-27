from __future__ import annotations

from capture_recovery.diff.structure_differ import StructureDiffer
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


def make_structure(
    *,
    name: str = "Object",
    offset: int = 0,
    length: int = 16,
    confidence: float = 1.0,
    metadata: dict | None = None,
    fields: list[Field] | None = None,
) -> Structure:
    return Structure(
        name=name,
        offset=offset,
        length=length,
        confidence=confidence,
        metadata={} if metadata is None else metadata,
        fields=[] if fields is None else fields,
    )


def make_field(
    *,
    name: str = "Value",
    offset: int = 0,
    length: int = 4,
    datatype: DataType = DataType.INT32,
    value=1,
) -> Field:
    return Field(
        name=name,
        offset=offset,
        length=length,
        datatype=datatype,
        value=value,
    )


def test_empty():
    differ = StructureDiffer()

    result = differ.compare([], [])

    assert result == ()


def test_identical_structures():
    differ = StructureDiffer()

    structure = make_structure(
        fields=[
            make_field(),
        ]
    )

    result = differ.compare([structure], [structure])

    assert result == ()


def test_structure_added():
    differ = StructureDiffer()

    after = make_structure(offset=100)

    result = differ.compare([], [after])

    assert len(result) == 1

    change = result[0]

    assert change.offset == 100
    assert change.structure_before is None
    assert change.structure_after == after
    assert change.changed_fields == ("added",)


def test_structure_removed():
    differ = StructureDiffer()

    before = make_structure(offset=100)

    result = differ.compare([before], [])

    assert len(result) == 1

    change = result[0]

    assert change.offset == 100
    assert change.structure_before == before
    assert change.structure_after is None
    assert change.changed_fields == ("removed",)


def test_name_changed():
    differ = StructureDiffer()

    before = make_structure(name="Old")
    after = make_structure(name="New")

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert result[0].changed_fields == ("name",)


def test_length_changed():
    differ = StructureDiffer()

    before = make_structure(length=16)
    after = make_structure(length=32)

    result = differ.compare([before], [after])

    assert result[0].changed_fields == ("length",)


def test_confidence_changed():
    differ = StructureDiffer()

    before = make_structure(confidence=0.50)
    after = make_structure(confidence=1.00)

    result = differ.compare([before], [after])

    assert result[0].changed_fields == ("confidence",)


def test_metadata_changed():
    differ = StructureDiffer()

    before = make_structure(metadata={"a": 1})
    after = make_structure(metadata={"a": 2})

    result = differ.compare([before], [after])

    assert result[0].changed_fields == ("metadata",)


def test_fields_changed():
    differ = StructureDiffer()

    before = make_structure(
        fields=[
            make_field(value=1),
        ]
    )

    after = make_structure(
        fields=[
            make_field(value=2),
        ]
    )

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert "fields" in result[0].changed_fields


def test_multiple_changes():
    differ = StructureDiffer()

    before = make_structure(
        name="Old",
        length=16,
        confidence=0.5,
        metadata={"x": 1},
        fields=[make_field(value=1)],
    )

    after = make_structure(
        name="New",
        length=32,
        confidence=1.0,
        metadata={"x": 2},
        fields=[make_field(value=2)],
    )

    result = differ.compare([before], [after])

    assert len(result) == 1

    assert set(result[0].changed_fields) == {
        "name",
        "length",
        "confidence",
        "metadata",
        "fields",
    }


def test_sorted():
    differ = StructureDiffer()

    before = [
        make_structure(offset=20),
        make_structure(offset=10),
    ]

    after = [
        make_structure(offset=20, length=32),
        make_structure(offset=10, length=32),
    ]

    result = differ.compare(before, after)

    assert len(result) == 2
    assert result[0].offset == 10
    assert result[1].offset == 20


def test_result_is_tuple():
    differ = StructureDiffer()

    result = differ.compare([], [])

    assert isinstance(result, tuple)