from capture_recovery.io import (
    CaptureBinaryReader,
)


def test_binary_reader(tmp_path):

    path = tmp_path / "capture.bin"

    path.write_bytes(
        b"123456"
    )

    reader = CaptureBinaryReader()

    assert reader.read(path) == b"123456"