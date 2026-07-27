import struct

from src.capture_recovery.detectors.integer_detector import IntegerDetector


def test_integer_detector_detects_integer():

    detector = IntegerDetector()

    data = struct.pack("<i", 12345)

    detections = detector.detect(data)

    assert len(detections) == 1

    detection = detections[0]

    assert detection.datatype == "int32"
    assert detection.offset == 0
    assert detection.length == 4
    assert detection.value == 12345
    assert detection.confidence == 0.85


def test_integer_detector_ignores_zero():

    detector = IntegerDetector()

    data = struct.pack("<i", 0)

    detections = detector.detect(data)

    assert detections == []


def test_integer_detector_ignores_negative():

    detector = IntegerDetector()

    data = struct.pack("<i", -1)

    detections = detector.detect(data)

    assert detections == []


def test_integer_detector_multiple():

    detector = IntegerDetector()

    data = (
        struct.pack("<i", 12)
        + struct.pack("<i", 34)
        + struct.pack("<i", 0)
        + struct.pack("<i", 56)
    )

    detections = detector.detect(data)

    assert len(detections) == 3

    first = detections[0]
    second = detections[1]
    third = detections[2]

    assert first.datatype == "int32"
    assert first.offset == 0
    assert first.length == 4
    assert first.value == 12

    assert second.datatype == "int32"
    assert second.offset == 4
    assert second.length == 4
    assert second.value == 34

    assert third.datatype == "int32"
    assert third.offset == 12
    assert third.length == 4
    assert third.value == 56