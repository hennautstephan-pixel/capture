from src.capture_recovery.indexes import DetectionIndex
from src.capture_recovery.models import Detection


def build_index():

    detections = [

        Detection("ascii", 10, 5, "Hello", 1.0),
        Detection("float", 30, 4, 1.25, 0.7),
        Detection("ascii", 40, 5, "World", 1.0),
        Detection("int32", 60, 4, 123, 0.8),

    ]

    return DetectionIndex(detections)


def test_by_type():

    index = build_index()

    assert len(index.by_type("ascii")) == 2


def test_at():

    index = build_index()

    assert len(index.at(30)) == 1
    assert index.at(30)[0].datatype == "float"


def test_before():

    index = build_index()

    assert len(index.before(40)) == 2


def test_after():

    index = build_index()

    assert len(index.after(40)) == 1
    assert index.after(40)[0].datatype == "int32"


def test_range():

    index = build_index()

    result = index.range(20, 50)

    assert len(result) == 2


def test_overlapping():

    index = build_index()

    result = index.overlapping(32, 34)

    assert len(result) == 1
    assert result[0].datatype == "float"