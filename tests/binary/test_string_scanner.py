from __future__ import annotations

import pytest

from capture_recovery.binary.string_scanner import (
    ExtractedString,
    StringScanner,
)


def test_empty_buffer() -> None:
    assert StringScanner.scan(b"") == []


def test_no_strings() -> None:
    data = bytes([0, 1, 2, 3, 4, 5])

    assert StringScanner.scan(data) == []


def test_ascii_string() -> None:
    data = b"\x00Hello World\x00"

    strings = StringScanner.scan(data)

    assert len(strings) == 1

    s = strings[0]

    assert s.offset == 1
    assert s.length == 11
    assert s.encoding == "ascii"
    assert s.text == "Hello World"


def test_two_ascii_strings() -> None:
    data = b"\x00Hello\x00World\x00"

    strings = StringScanner.scan(data)

    assert len(strings) == 2

    assert strings[0].text == "Hello"
    assert strings[0].offset == 1

    assert strings[1].text == "World"
    assert strings[1].offset == 7


def test_ascii_at_end() -> None:
    data = b"\x00Test"

    strings = StringScanner.scan(data)

    assert len(strings) == 1
    assert strings[0].text == "Test"


def test_utf16_le() -> None:
    data = (
        b"\x00"
        + "Capture".encode("utf-16le")
        + b"\x00"
    )

    strings = StringScanner.scan(data)

    utf16 = [s for s in strings if s.encoding == "utf-16le"]

    assert len(utf16) == 1
    assert utf16[0].text == "Capture"


def test_utf16_be() -> None:
    data = (
        b"\x00"
        + "Capture".encode("utf-16be")
        + b"\x00"
    )

    strings = StringScanner.scan(data)

    utf16 = [s for s in strings if s.encoding == "utf-16be"]

    assert len(utf16) == 1
    assert utf16[0].text == "Capture"


def test_bytearray() -> None:
    data = bytearray(b"\x00Capture\x00")

    strings = StringScanner.scan(data)

    assert len(strings) == 1
    assert strings[0].text == "Capture"


def test_memoryview() -> None:
    data = memoryview(b"\x00Capture\x00")

    strings = StringScanner.scan(data)

    assert len(strings) == 1
    assert strings[0].text == "Capture"


def test_minimum_length_default() -> None:
    data = b"\x00abc\x00"

    strings = StringScanner.scan(data)

    assert strings == []


def test_minimum_length_custom() -> None:
    data = b"\x00abc\x00"

    strings = StringScanner.scan(
        data,
        minimum_length=3,
    )

    assert len(strings) == 1
    assert strings[0].text == "abc"


def test_invalid_minimum_length() -> None:
    with pytest.raises(ValueError):
        StringScanner.scan(
            b"abcd",
            minimum_length=0,
        )


def test_result_order() -> None:
    data = (
        b"\x00"
        + b"AAAA"
        + b"\x00"
        + "BBBB".encode("utf-16le")
        + b"\x00"
        + b"CCCC"
    )

    strings = StringScanner.scan(data)

    offsets = [s.offset for s in strings]

    assert offsets == sorted(offsets)


def test_extracted_string_dataclass() -> None:
    s = ExtractedString(
        offset=10,
        length=5,
        encoding="ascii",
        text="Hello",
    )

    assert s.offset == 10
    assert s.length == 5
    assert s.encoding == "ascii"
    assert s.text == "Hello"


def test_ascii_with_spaces() -> None:
    data = b"\x00The quick brown fox\x00"

    strings = StringScanner.scan(data)

    assert len(strings) == 1
    assert strings[0].text == "The quick brown fox"


def test_multiple_encodings() -> None:
    data = (
        b"\x00ASCII\x00"
        + "UTF16".encode("utf-16le")
        + b"\x00"
        + "BE".encode("utf-16be")
    )

    strings = StringScanner.scan(data)

    assert any(s.encoding == "ascii" for s in strings)
    assert any(s.encoding == "utf-16le" for s in strings)
    assert any(s.encoding == "utf-16be" for s in strings)


def test_scan_returns_list() -> None:
    result = StringScanner.scan(b"Hello")

    assert isinstance(result, list)


def test_offsets_are_positive() -> None:
    strings = StringScanner.scan(b"\x00Hello\x00World\x00")

    assert all(s.offset >= 0 for s in strings)


def test_lengths_match_text() -> None:
    strings = StringScanner.scan(b"\x00Capture Recovery\x00")

    assert all(s.length == len(s.text) for s in strings)