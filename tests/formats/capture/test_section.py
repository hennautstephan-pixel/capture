from __future__ import annotations

from capture_recovery.formats.capture import (
    CaptureSection,
)


def make_section() -> CaptureSection:
    return CaptureSection(
        offset=100,
        size=32,
        raw=b"\x01" * 32,
    )


def test_fields():

    section = make_section()

    assert section.offset == 100
    assert section.size == 32
    assert len(section.raw) == 32


def test_len():

    section = make_section()

    assert len(section) == 32


def test_end_offset():

    section = make_section()

    assert section.end_offset == 132


def test_contains():

    section = make_section()

    assert section.contains(100)
    assert section.contains(120)
    assert section.contains(131)

    assert not section.contains(99)
    assert not section.contains(132)


def test_is_empty_false():

    section = make_section()

    assert not section.is_empty


def test_is_empty_true():

    section = CaptureSection(
        offset=0,
        size=0,
        raw=b"",
    )

    assert section.is_empty


def test_equality():

    a = make_section()
    b = make_section()

    assert a == b


def test_hashable():

    section = make_section()

    assert hash(section)


def test_repr():

    section = make_section()

    text = repr(section)

    assert "CaptureSection" in text
    assert "offset=100" in text
    assert "size=32" in text