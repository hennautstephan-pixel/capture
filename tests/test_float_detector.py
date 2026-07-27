import math
import struct

from src.capture_recovery.detectors.float_detector import FloatDetector


def test_float_detector_detects_one():

    detector = FloatDetector()

    data = struct.pack("<f", 123.5)

    detections = detector.detect(data)

    assert len(detections) == 1

    detection = detections[0]

    assert detection.datatype == "float"
    assert detection.offset == 0
    assert detection.length == 4
    assert math.isclose(detection.value, 123.5)
    assert detection.confidence == 0.70


def test_float_detector_rejects_short_buffer():

    detector = FloatDetector()

    detections = detector.detect(b"\x00\x00")

    assert detections == []


def test_float_detector_rejects_nan():

    detector = FloatDetector()

    data = struct.pack("<I", 0x7FC00000)

    detections = detector.detect(data)

    assert detections == []