from __future__ import annotations

from capture_recovery.formats.capture import CaptureHeader


def make_header() -> CaptureHeader:
    return CaptureHeader(
        file_size=1234,
        project_tag="Project",
        format_version=1,
        software_tag="SoftwareVersion",
        software_tag_version=4,
        first_stream_offset=72,
    )


def test_header_fields():

    header = make_header()

    assert header.file_size == 1234
    assert header.project_tag == "Project"
    assert header.format_version == 1
    assert header.software_tag == "SoftwareVersion"
    assert header.software_tag_version == 4
    assert header.first_stream_offset == 72


def test_validate_size_true():

    header = make_header()

    assert header.validate_size(1234)


def test_validate_size_false():

    header = make_header()

    assert not header.validate_size(2048)


def test_header_is_hashable():

    header = make_header()

    assert hash(header)


def test_header_equality():

    a = make_header()
    b = make_header()

    assert a == b


def test_header_repr():

    header = make_header()

    text = repr(header)

    assert "CaptureHeader" in text
    assert "1234" in text

def test_header_size():

    header = make_header()

    assert header.header_size == 0

def test_reserved_bytes():

    header = CaptureHeader(
        file_size=1,
        project_tag="Project",
        format_version=1,
        software_tag="SoftwareVersion",
        software_tag_version=4,
        first_stream_offset=72,
        reserved=b"\x01\x02",
    )

    assert header.has_reserved_bytes

def test_reserved_empty():

    header = make_header()

    assert not header.has_reserved_bytes

def test_validate():

    header = make_header()

    assert header.validate(1234) == ()

def test_validate_invalid_size():

    header = make_header()

    errors = header.validate(5)

    assert "Invalid file size." in errors

def test_is_valid():

    assert make_header().is_valid