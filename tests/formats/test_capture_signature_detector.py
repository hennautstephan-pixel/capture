from capture_recovery.formats import (
    CaptureSignatureDetector,
)



def test_capture_signature_detector():


    detector = CaptureSignatureDetector(
        window_size=8
    )


    data = (
        b"ABCDEFGH"
        +
        b"12345678"
        +
        b"ABCDEFGH"
    )


    result = detector.detect(
        data
    )


    assert result["count"] >= 1


    signature = result["signatures"][0]


    assert (
        signature["occurrences"]
        >= 2
    )


    assert (
        signature["size"]
        == 8
    )