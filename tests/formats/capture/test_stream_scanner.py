from __future__ import annotations

from capture_recovery.formats.capture import (
    CaptureStreamScanner,
)


def test_default_signatures():

    scanner = CaptureStreamScanner()

    assert len(scanner.signatures) == 4


def test_find_single_stream():

    scanner = CaptureStreamScanner()

    data = (
        b"\x00" * 10
        + b"\x78\x9C"
        + b"\x00" * 5
    )

    assert scanner.find(data) == [10]


def test_find_multiple_streams():

    scanner = CaptureStreamScanner()

    data = (
        b"\x78\x9C"
        + b"\x00" * 8
        + b"\x78\xDA"
        + b"\x00" * 6
        + b"\x78\x01"
    )

    assert scanner.find(data) == [
        0,
        10,
        18,
    ]


def test_find_none():

    scanner = CaptureStreamScanner()

    assert scanner.find(b"\x00" * 100) == []


def test_first():

    scanner = CaptureStreamScanner()

    data = (
        b"\x00" * 5
        + b"\x78\x9C"
        + b"\x00"
    )

    assert scanner.first(data) == 5


def test_first_none():

    scanner = CaptureStreamScanner()

    assert scanner.first(b"\x00" * 20) is None


def test_custom_signature():

    scanner = CaptureStreamScanner(
        signatures=[b"\xAA\xBB"],
    )

    assert scanner.find(
        b"\x00\xAA\xBB\x00"
    ) == [1]


def test_empty_data():

    scanner = CaptureStreamScanner()

    assert scanner.find(b"") == []