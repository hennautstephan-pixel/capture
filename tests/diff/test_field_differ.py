from __future__ import annotations

from capture_recovery.diff.field_differ import FieldDiffer
from capture_recovery.models import DataType
from capture_recovery.structures.field import Field


def test_empty():
    differ = FieldDiffer()

    result = differ.compare([], [])

    assert result == ()


def test_identical_fields():
    differ = FieldDiffer()

    field = Field(
        name="Position",
        offset=100,
        length=4,
        datatype=DataType.FLOAT32,
        value=12.5,
    )

    result = differ.compare([field], [field])

    assert result == ()


def test_field_added():
    differ = FieldDiffer()

    after = Field(
        name="Intensity",
        offset=20,
        length=4,
        datatype=DataType.FLOAT32,
        value=1.0,
    )

    result = differ.compare([], [after])

    assert len(result) == 1

    change = result[0]

    assert change.offset == 20
    assert change.field_before is None
    assert change.field_after == after
    assert change.changed_properties == ("added",)


def test_field_removed():
    differ = FieldDiffer()

    before = Field(
        name="Intensity",
        offset=20,
        length=4,
        datatype=DataType.FLOAT32,
        value=1.0,
    )

    result = differ.compare([before], [])

    assert len(result) == 1

    change = result[0]

    assert change.offset == 20
    assert change.field_before == before
    assert change.field_after is None
    assert change.changed_properties == ("removed",)


def test_name_changed():
    differ = FieldDiffer()

    before = Field(
        name="Old",
        offset=10,
        length=4,
        datatype=DataType.INT32,
        value=1,
    )

    after = Field(
        name="New",
        offset=10,
        length=4,
        datatype=DataType.INT32,
        value=1,
    )

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert result[0].changed_properties == ("name",)


def test_datatype_changed():
    differ = FieldDiffer()

    before = Field(
        name="Value",
        offset=8,
        length=4,
        datatype=DataType.INT32,
        value=12,
    )

    after = Field(
        name="Value",
        offset=8,
        length=4,
        datatype=DataType.FLOAT32,
        value=12,
    )

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert result[0].changed_properties == ("datatype",)


def test_length_changed():
    differ = FieldDiffer()

    before = Field(
        name="Name",
        offset=50,
        length=4,
        datatype=DataType.ASCII,
        value="ABCD",
    )

    after = Field(
        name="Name",
        offset=50,
        length=8,
        datatype=DataType.ASCII,
        value="ABCDEFGH",
    )

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert result[0].changed_properties == ("length", "value")


def test_value_changed():
    differ = FieldDiffer()

    before = Field(
        name="Intensity",
        offset=40,
        length=4,
        datatype=DataType.FLOAT32,
        value=1.0,
    )

    after = Field(
        name="Intensity",
        offset=40,
        length=4,
        datatype=DataType.FLOAT32,
        value=2.0,
    )

    result = differ.compare([before], [after])

    assert len(result) == 1
    assert result[0].changed_properties == ("value",)


def test_multiple_changes():
    differ = FieldDiffer()

    before = Field(
        name="Old",
        offset=100,
        length=4,
        datatype=DataType.INT32,
        value=10,
    )

    after = Field(
        name="New",
        offset=100,
        length=8,
        datatype=DataType.FLOAT32,
        value=10.5,
    )

    result = differ.compare([before], [after])

    assert len(result) == 1

    assert set(result[0].changed_properties) == {
        "name",
        "length",
        "datatype",
        "value",
    }


def test_sorted():
    differ = FieldDiffer()

    before = [
        Field(
            name="B",
            offset=20,
            length=4,
            datatype=DataType.INT32,
            value=1,
        ),
        Field(
            name="A",
            offset=10,
            length=4,
            datatype=DataType.INT32,
            value=2,
        ),
    ]

    after = [
        Field(
            name="B",
            offset=20,
            length=4,
            datatype=DataType.INT32,
            value=3,
        ),
        Field(
            name="A",
            offset=10,
            length=4,
            datatype=DataType.INT32,
            value=4,
        ),
    ]

    result = differ.compare(before, after)

    assert len(result) == 2
    assert result[0].offset == 10
    assert result[1].offset == 20


def test_result_is_tuple():
    differ = FieldDiffer()

    result = differ.compare([], [])

    assert isinstance(result, tuple)