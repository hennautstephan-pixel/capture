from src.capture_recovery.detectors.ascii_detector import AsciiDetector


def test_ascii_detector():

    detector = AsciiDetector()

    data = (
        b"\x00\x01"
        b"Hello"
        b"\x00"
        b"World"
        b"\x00"
    )

    detections = detector.detect(data)

    assert len(detections) == 2

    first = detections[0]
    second = detections[1]

    #
    # Première chaîne
    #

    assert first.datatype == "ascii"
    assert first.offset == 2
    assert first.length == 5
    assert first.value == "Hello"
    assert first.confidence == 1.0

    #
    # Seconde chaîne
    #

    assert second.datatype == "ascii"
    assert second.offset == 8
    assert second.length == 5
    assert second.value == "World"
    assert second.confidence == 1.0