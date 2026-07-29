from capture_recovery.models import Detection
from capture_recovery.parser.detection_adapter import DetectionAdapter


def test_convert_single_detection():

    detection = Detection(
        datatype="ascii",
        offset=10,
        length=5,
        value="Hello",
        confidence=1.0,
    )

    segment = DetectionAdapter.to_segment(detection)

    assert segment.kind == "ascii"
    assert segment.offset == 10
    assert segment.length == 5
    assert segment.confidence == 1.0
    assert segment.metadata["value"] == "Hello"


def test_convert_list():

    detections = [
        Detection(
            datatype="ascii",
            offset=0,
            length=4,
            value="Test",
            confidence=0.9,
        )
    ]

    segments = DetectionAdapter.to_segments(detections)

    assert len(segments) == 1
    assert segments[0].kind == "ascii"


def test_empty_list():

    assert DetectionAdapter.to_segments([]) == []


def test_none_value():

    detection = Detection(
        datatype="binary",
        offset=20,
        length=32,
        value=None,
        confidence=0.5,
    )

    segment = DetectionAdapter.to_segment(detection)

    assert segment.metadata == {}