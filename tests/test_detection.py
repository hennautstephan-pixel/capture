from capture_recovery.models import DataType
from capture_recovery.models import Detection


def test_end():

    d = Detection(
        offset=100,
        length=20,
        datatype=DataType.ASCII,
        value="abc",
    )

    assert d.end == 120


def test_contains():

    d = Detection(
        offset=10,
        length=10,
        datatype=DataType.INT32,
        value=123,
    )

    assert d.contains(10)
    assert d.contains(19)

    assert not d.contains(20)


def test_overlap():

    a = Detection(
        offset=0,
        length=20,
        datatype=DataType.BYTES,
        value=None,
    )

    b = Detection(
        offset=10,
        length=20,
        datatype=DataType.BYTES,
        value=None,
    )

    assert a.overlaps(b)


def test_copy():

    d = Detection(
        offset=0,
        length=4,
        datatype=DataType.FLOAT32,
        value=1.5,
    )

    c = d.copy(confidence=0.5)

    assert c.confidence == 0.5

    assert c.offset == d.offset

    assert c.datatype == d.datatype


def test_len():

    d = Detection(
        offset=0,
        length=42,
        datatype=DataType.BYTES,
        value=None,
    )

    assert len(d) == 42