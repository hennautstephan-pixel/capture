from src.capture_recovery.detectors.signature_detector import SignatureDetector


def test_signature_detector_zip():

    detector = SignatureDetector()

    data = (
        b"\x00\x00"
        b"PK\x03\x04"
        b"\x01\x02"
    )

    detections = detector.detect(data)

    assert len(detections) == 1

    detection = detections[0]

    assert detection.datatype == "zip"
    assert detection.offset == 2
    assert detection.length == 4
    assert detection.value is None
    assert detection.confidence == 1.0


def test_signature_detector_multiple_zip():

    detector = SignatureDetector()

    data = (
        b"PK\x03\x04"
        b"\x00\x00"
        b"PK\x03\x04"
    )

    detections = detector.detect(data)

    assert len(detections) == 2

    first = detections[0]
    second = detections[1]

    assert first.datatype == "zip"
    assert first.offset == 0
    assert first.length == 4
    assert first.value is None

    assert second.datatype == "zip"
    assert second.offset == 6
    assert second.length == 4
    assert second.value is None


def test_signature_detector_png():

    detector = SignatureDetector()

    data = (
        b"\x00\x00"
        b"\x89PNG"
        b"\x00"
    )

    detections = detector.detect(data)

    assert len(detections) == 1

    detection = detections[0]

    assert detection.datatype == "png"
    assert detection.offset == 2
    assert detection.length == 4
    assert detection.value is None
    assert detection.confidence == 1.0