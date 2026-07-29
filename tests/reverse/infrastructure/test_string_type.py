"""
Tests for capture_recovery.reverse.string_type.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.string_type import (
    ASCII,
    STRING_TYPES,
    UTF8,
    UTF16_BE,
    UTF16_LE,
    StringType,
)


# ----------------------------------------------------------------------
# Creation
# ----------------------------------------------------------------------


def test_create_string_type() -> None:

    value = StringType(
        name="test",
        encoding="ascii",
        char_width=1,
    )

    assert value.name == "test"
    assert value.encoding == "ascii"
    assert value.char_width == 1



def test_default_null_terminated() -> None:

    value = StringType(
        name="test",
        encoding="ascii",
        char_width=1,
    )

    assert value.null_terminated is True



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_empty_name_rejected() -> None:

    with pytest.raises(ValueError):

        StringType(
            name="",
            encoding="ascii",
            char_width=1,
        )



def test_empty_encoding_rejected() -> None:

    with pytest.raises(ValueError):

        StringType(
            name="test",
            encoding="",
            char_width=1,
        )



def test_invalid_char_width_rejected() -> None:

    with pytest.raises(ValueError):

        StringType(
            name="test",
            encoding="ascii",
            char_width=0,
        )



# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_ascii_is_single_byte() -> None:

    assert ASCII.is_single_byte is True



def test_utf16_is_wide() -> None:

    assert UTF16_LE.is_wide is True



def test_utf8_not_wide() -> None:

    assert UTF8.is_wide is False



# ----------------------------------------------------------------------
# Standard definitions
# ----------------------------------------------------------------------


def test_ascii_definition() -> None:

    assert ASCII.name == "ascii"
    assert ASCII.encoding == "ascii"
    assert ASCII.char_width == 1



def test_utf8_definition() -> None:

    assert UTF8.encoding == "utf-8"



def test_utf16_le_definition() -> None:

    assert UTF16_LE.encoding == "utf-16-le"



def test_utf16_be_definition() -> None:

    assert UTF16_BE.encoding == "utf-16-be"



# ----------------------------------------------------------------------
# Collection
# ----------------------------------------------------------------------


def test_string_types_count() -> None:

    assert len(STRING_TYPES) == 4



def test_string_type_names_unique() -> None:

    names = {
        item.name
        for item in STRING_TYPES
    }

    assert len(names) == len(
        STRING_TYPES
    )



# ----------------------------------------------------------------------
# Immutability
# ----------------------------------------------------------------------


def test_string_type_is_frozen() -> None:

    with pytest.raises(AttributeError):

        ASCII.name = "changed"