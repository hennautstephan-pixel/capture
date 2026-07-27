from src.capture_recovery.indexes import DetectionIndex
from src.capture_recovery.models import DataType
from src.capture_recovery.models import Detection


def build_index():

    detections = [

        Detection(
            offset=10,
            length=5,
            datatype=DataType.ASCII,
            value="Hello",
            confidence=1.0,
        ),

        Detection(
            offset=30,
            length=4,
            datatype=DataType.FLOAT32,
            value=1.25,
            confidence=0.7,
        ),

        Detection(
            offset=40,
            length=5,
            datatype=DataType.ASCII,
            value="World",
            confidence=1.0,
        ),

        Detection(
            offset=60,
            length=4,
            datatype=DataType.INT32,
            value=123,
            confidence=0.8,
        ),

    ]

    return DetectionIndex(detections)


def test_by_type():

    index = build_index()

    assert len(index.by_type(DataType.ASCII)) == 2


def test_at():

    index = build_index()

    result = index.at(30)

    assert len(result) == 1
    assert result[0].datatype == DataType.FLOAT32


def test_before():

    index = build_index()

    assert len(index.before(40)) == 2


def test_after():

    index = build_index()

    result = index.after(40)

    assert len(result) == 1
    assert result[0].datatype == DataType.INT32


def test_range():

    index = build_index()

    result = index.range(20, 50)

    assert len(result) == 2


def test_overlapping():

    index = build_index()

    result = index.overlapping(32, 34)

    assert len(result) == 1
    assert result[0].datatype == DataType.FLOAT32