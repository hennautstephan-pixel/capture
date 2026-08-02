from pathlib import Path

from capture_recovery.tools import (
    StreamInspection,
)


def test_properties():

    inspection = StreamInspection(
        file=Path("sample.c2p"),
        compressed_size=100,
        decompressed_size=200,
        printable_bytes=50,
        zero_bytes=20,
        printable_ratio=0.25,
        zero_ratio=0.10,
        first_bytes=b"abcd",
    )

    assert inspection.compressed_size == 100

    assert inspection.decompressed_size == 200

    assert not inspection.is_empty


def test_empty():

    inspection = StreamInspection(
        file=Path("empty.c2p"),
        compressed_size=0,
        decompressed_size=0,
        printable_bytes=0,
        zero_bytes=0,
        printable_ratio=0.0,
        zero_ratio=0.0,
        first_bytes=b"",
    )

    assert inspection.is_empty