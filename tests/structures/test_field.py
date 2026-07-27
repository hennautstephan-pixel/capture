from capture_recovery.models import DataType
from capture_recovery.structures import Field


def test_end():

    f = Field(
        name="x",
        offset=100,
        length=4,
        datatype=DataType.FLOAT32,
    )

    assert f.end == 104


def test_contains():

    f = Field(
        name="x",
        offset=10,
        length=5,
        datatype=DataType.INT32,
    )

    assert f.contains(10)
    assert f.contains(14)

    assert not f.contains(15)