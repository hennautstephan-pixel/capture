from capture_recovery.io import (
    CaptureFormatDetector,
)


def test_detect_capture_binary(
    tmp_path,
):

    file = tmp_path / "project.cap"


    file.write_bytes(
        b"CAPTURE"
        + b"\x00\x01\x02",
    )


    result = (
        CaptureFormatDetector()
        .detect(
            file,
        )
    )


    assert result == (
        "capture_binary"
    )



def test_detect_json(
    tmp_path,
):

    file = tmp_path / "project.json"


    file.write_bytes(
        b"{\"name\":\"test\"}"
    )


    result = (
        CaptureFormatDetector()
        .detect(
            file,
        )
    )


    assert result == (
        "json"
    )



def test_detect_unknown(
    tmp_path,
):

    file = tmp_path / "unknown.bin"


    file.write_bytes(
        b"XXXX"
    )


    result = (
        CaptureFormatDetector()
        .detect(
            file,
        )
    )


    assert result == (
        "unknown"
    )