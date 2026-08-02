from __future__ import annotations

import zlib

from capture_recovery.formats.capture import (
    CaptureStreamLocator,
)


def test_no_stream():

    locator = CaptureStreamLocator()

    assert locator.locate(b"") == []


def test_single_stream():

    locator = CaptureStreamLocator()

    data = (
        b"\x00" * 8
        + b"\x78\x9C"
        + b"\xAA\xBB"
    )

    regions = locator.locate(data)

    assert len(regions) == 1

    region = regions[0]

    assert region.start == 8
    assert region.end == len(data)
    assert region.signature == b"\x78\x9C"


def test_multiple_streams():

    locator = CaptureStreamLocator()

    data = (
        b"\x78\x9C"
        + b"\x00" * 5
        + b"\x78\xDA"
        + b"\x00" * 3
    )

    regions = locator.locate(data)

    assert len(regions) == 2

    assert regions[0].start == 0
    assert regions[0].end == 7

    assert regions[1].start == 7
    assert regions[1].end == len(data)


def test_first():

    locator = CaptureStreamLocator()

    data = (
        b"\x00" * 5
        + b"\x78\x01"
    )

    region = locator.first(data)

    assert region is not None
    assert region.start == 5


def test_first_none():

    locator = CaptureStreamLocator()

    assert locator.first(b"") is None


def test_scanner_property():

    locator = CaptureStreamLocator()

    assert locator.scanner is not None

def test_region_reports_consumed_bytes():

    locator = CaptureStreamLocator()

    compressed = zlib.compress(
        b"A" * 200
    )

    data = (
        b"\x00" * 20
        + compressed
        + b"FOOTER"
    )

    region = locator.first(data)

    assert region is not None

    assert region.bytes_consumed == len(compressed)

    assert region.end == (
        region.start + len(compressed)
    )