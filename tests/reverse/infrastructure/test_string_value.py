"""
Tests for capture_recovery.reverse.string_value.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.string_type import (
    ASCII,
    UTF8,
    UTF16_LE,
)

from capture_recovery.reverse.string_value import (
    StringValue,
)



def create_ascii_value() -> StringValue:

    return StringValue(
        offset=10,
        string_type=ASCII,
        value="Hello",
        raw_bytes=b"Hello",
        terminated=True,
    )



# ----------------------------------------------------------------------
# Creation
# ----------------------------------------------------------------------


def test_create_string_value() -> None:

    value = create_ascii_value()

    assert value.offset == 10
    assert value.value == "Hello"



def test_raw_bytes_kept() -> None:

    value = create_ascii_value()

    assert value.raw_bytes == b"Hello"



def test_termination_flag() -> None:

    value = create_ascii_value()

    assert value.terminated is True



# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_length() -> None:

    value = create_ascii_value()

    assert value.length == 5



def test_char_length() -> None:

    value = create_ascii_value()

    assert value.char_length == 5



def test_type_name() -> None:

    value = create_ascii_value()

    assert value.type_name == "ascii"



def test_encoding() -> None:

    value = create_ascii_value()

    assert value.encoding == "ascii"



# ----------------------------------------------------------------------
# Encoding helpers
# ----------------------------------------------------------------------


def test_is_ascii() -> None:

    value = create_ascii_value()

    assert value.is_ascii is True



def test_is_utf8() -> None:

    value = StringValue(
        offset=0,
        string_type=UTF8,
        value="hello",
        raw_bytes=b"hello",
    )

    assert value.is_utf8 is True



def test_is_utf16() -> None:

    value = StringValue(
        offset=0,
        string_type=UTF16_LE,
        value="hello",
        raw_bytes=b"h\x00",
    )

    assert value.is_utf16 is True



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_negative_offset_rejected() -> None:

    with pytest.raises(ValueError):

        StringValue(
            offset=-1,
            string_type=ASCII,
            value="test",
            raw_bytes=b"test",
        )



def test_value_must_be_string() -> None:

    with pytest.raises(TypeError):

        StringValue(
            offset=0,
            string_type=ASCII,
            value=123,
            raw_bytes=b"123",
        )



def test_raw_bytes_must_be_bytes() -> None:

    with pytest.raises(TypeError):

        StringValue(
            offset=0,
            string_type=ASCII,
            value="test",
            raw_bytes="test",
        )



# ----------------------------------------------------------------------
# Serialization
# ----------------------------------------------------------------------


def test_as_dict() -> None:

    value = create_ascii_value()

    result = value.as_dict()

    assert result["offset"] == 10
    assert result["type"] == "ascii"
    assert result["value"] == "Hello"
    assert result["length"] == 5