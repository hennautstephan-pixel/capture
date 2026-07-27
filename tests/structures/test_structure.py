from capture_recovery.models import DataType
from capture_recovery.structures import Field
from capture_recovery.structures import Structure


def test_add():

    s = Structure(
        name="Transform",
        offset=100,
        length=64,
    )

    s.add(
        Field(
            name="x",
            offset=100,
            length=4,
            datatype=DataType.FLOAT32,
        )
    )

    assert len(s.fields) == 1


def test_sort():

    s = Structure(
        name="Test",
        offset=0,
        length=32,
    )

    s.add(
        Field(
            "b",
            8,
            4,
            DataType.INT32,
        )
    )

    s.add(
        Field(
            "a",
            0,
            4,
            DataType.INT32,
        )
    )

    s.sort()

    assert s.fields[0].name == "a"


def test_iter():

    s = Structure(
        name="A",
        offset=0,
        length=16,
    )

    s.add(
        Field(
            "x",
            0,
            4,
            DataType.INT32,
        )
    )

    assert len(list(s)) == 1