from __future__ import annotations

from capture_recovery.formats.capture import (
    CaptureStream,
    CaptureStreamParser,
    stream,
)


def test_parse_empty():

    parser = CaptureStreamParser()

    assert parser.parse(b"") == []


def test_parse_single():

    parser = CaptureStreamParser()

    data = (
        b"\x00" * 8
        + b"\x78\x9C"
        + b"\xAA\xBB"
    )

    streams = parser.parse(data)

    assert len(streams) == 1

    stream = streams[0]

    assert isinstance(
        stream,
        CaptureStream,
    )

    assert stream.offset == 8
    assert stream.compression == "zlib"
    assert stream.compressed_size == 4
    assert stream.raw == b"\x78\x9C\xAA\xBB"


def test_parse_multiple():

    parser = CaptureStreamParser()

    data = (
        b"\x78\x9C"
        + b"\x00" * 5
        + b"\x78\xDA"
    )

    streams = parser.parse(data)

    assert len(streams) == 2

    assert streams[0].offset == 0
    assert streams[0].compression == "zlib"

    assert streams[1].offset == 7
    assert streams[1].compression == "zlib-9"


def test_first():

    parser = CaptureStreamParser()

    data = (
        b"\x00" * 12
        + b"\x78\x01"
    )

    stream = parser.first(data)

    assert stream is not None
    assert stream.offset == 12


def test_first_none():

    parser = CaptureStreamParser()

    assert parser.first(b"") is None


def test_parser_scanner_property():

    parser = CaptureStreamParser()

    assert parser.scanner is not None

def test_region_size_used():

    parser = CaptureStreamParser()

    data = (
        b"\x78\x9C"
        + b"\x00" * 5
        + b"\x78\xDA"
        + b"\x00" * 3
    )

    streams = parser.parse(data)

    assert streams[0].compressed_size == 7
    assert len(streams[0].raw) == 7

    assert streams[1].compressed_size == 5
    assert len(streams[1].raw) == 5

def test_locator_property():

    parser = CaptureStreamParser()

    assert parser.locator is not None