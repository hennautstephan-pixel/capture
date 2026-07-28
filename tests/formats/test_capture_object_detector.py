from capture_recovery.formats import (
    CaptureObjectDetector,
)



def test_capture_object_detector():


    detector = CaptureObjectDetector()



    data = (

        b"\x20\x00\x00\x00"

        +

        b"A" * 28

        +

        b"\x10\x00\x00\x00"

        +

        b"B" * 12

    )



    result = detector.detect(
        data
    )



    assert len(
        result
    ) >= 1



    assert result[0]["size"] == 32



    assert (
        "confidence"
        in result[0]
    )