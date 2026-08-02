from __future__ import annotations

import struct

import pytest

from capture_recovery.formats.capture import (
    CaptureHeader,
    CaptureHeaderParser,
)


PROJECT = b"Project\x00"
SOFTWARE = b"SoftwareVersion\x00"


def build_header(
    *,
    file_size: int = 1024,
) -> bytes:

    data = bytearray(128)

    struct.pack_into("<I", data, 0, file_size)

    data[4:12] = PROJECT

    struct.pack_into("<I", data, 16, 1)

    start = 20

    data[start:start + len(SOFTWARE)] = SOFTWARE

    version_offset = start + len(SOFTWARE)

    struct.pack_into("<I", data, version_offset, 4)

    data[72:74] = b"\x78\x9c"

    return bytes(data)


def test_parse_header():

    parser = CaptureHeaderParser()

    header = parser.parse(
        build_header(file_size=4096)
    )

    assert isinstance(
        header,
        CaptureHeader,
    )

    assert header.file_size == 4096
    assert header.project_tag == "Project"
    assert header.format_version == 1
    assert header.software_tag == "SoftwareVersion"
    assert header.software_tag_version == 4
    assert header.first_stream_offset == 72
    assert header.header_size == 72
    assert header.raw == build_header(file_size=4096)[:72]
    assert header.reserved

def test_header_is_valid():

    parser = CaptureHeaderParser()

    header = parser.parse(
        build_header()
    )

    assert header.is_valid


def test_validate_size():

    parser = CaptureHeaderParser()

    header = parser.parse(
        build_header(file_size=512)
    )

    assert header.validate_size(512)
    assert not header.validate_size(1024)


def test_invalid_project_signature():

    parser = CaptureHeaderParser()

    data = bytearray(build_header())

    data[4:12] = b"Invalid!"

    with pytest.raises(ValueError):
        parser.parse(bytes(data))


def test_missing_zlib_signature():

    parser = CaptureHeaderParser()

    data = bytearray(build_header())

    data[72:74] = b"\x00\x00"

    with pytest.raises(ValueError):
        parser.parse(bytes(data))


def test_file_too_small():

    parser = CaptureHeaderParser()

    with pytest.raises(ValueError):
        parser.parse(b"\x00" * 16)