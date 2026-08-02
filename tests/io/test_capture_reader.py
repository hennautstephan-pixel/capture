from capture_recovery.io import (
    CaptureReader,
)


def test_reader_creation():

    reader = CaptureReader()

    assert isinstance(
        reader,
        CaptureReader,
    )


def test_read_bytes(tmp_path):

    path = tmp_path / "test.bin"

    path.write_bytes(
        b"abcd"
    )

    result = CaptureReader().read_bytes(
        path,
    )

    assert result == b"abcd"


def test_detect_unknown(tmp_path):

    path = tmp_path / "unknown.bin"

    path.write_bytes(
        b"XXXX"
    )

    result = CaptureReader().detect_format(
        path,
    )

    assert result == "unknown"