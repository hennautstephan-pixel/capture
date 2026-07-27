from src.capture_recovery.models import Detection


def test_detection_creation():

    detection = Detection(
        datatype="float",
        offset=0,
        length=4,
        value=1.0,
        confidence=0.75,
    )

    assert detection.datatype == "float"
    assert detection.offset == 0
    assert detection.length == 4
    assert detection.value == 1.0
    assert detection.confidence == 0.75