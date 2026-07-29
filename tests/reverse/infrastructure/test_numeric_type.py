"""
Tests for capture_recovery.reverse.numeric_type.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.numeric_type import (
    FLOAT32,
    FLOAT64,
    INT16,
    INT32,
    INT64,
    NUMERIC_TYPES,
    UINT16,
    UINT32,
    UINT64,
    NumericType,
)


# ----------------------------------------------------------------------
# NumericType creation
# ----------------------------------------------------------------------


def test_create_integer_type() -> None:

    numeric_type = NumericType(
        name="test_int",
        struct_format="i",
        size=4,
        floating=False,
        signed=True,
    )

    assert numeric_type.name == "test_int"
    assert numeric_type.struct_format == "i"
    assert numeric_type.size == 4
    assert numeric_type.signed is True


def test_create_float_type() -> None:

    numeric_type = NumericType(
        name="test_float",
        struct_format="f",
        size=4,
        floating=True,
    )

    assert numeric_type.floating is True
    assert numeric_type.signed is None


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_empty_name_rejected() -> None:

    with pytest.raises(ValueError):

        NumericType(
            name="",
            struct_format="i",
            size=4,
            floating=False,
        )


def test_empty_struct_format_rejected() -> None:

    with pytest.raises(ValueError):

        NumericType(
            name="test",
            struct_format="",
            size=4,
            floating=False,
        )


def test_zero_size_rejected() -> None:

    with pytest.raises(ValueError):

        NumericType(
            name="test",
            struct_format="i",
            size=0,
            floating=False,
        )


def test_negative_size_rejected() -> None:

    with pytest.raises(ValueError):

        NumericType(
            name="test",
            struct_format="i",
            size=-1,
            floating=False,
        )


def test_float_cannot_define_signedness() -> None:

    with pytest.raises(ValueError):

        NumericType(
            name="bad_float",
            struct_format="f",
            size=4,
            floating=True,
            signed=True,
        )


# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_integer_type_is_integer() -> None:

    assert INT32.is_integer is True


def test_integer_type_is_not_float() -> None:

    assert INT32.is_float is False


def test_float_type_is_float() -> None:

    assert FLOAT32.is_float is True


def test_float_type_is_not_integer() -> None:

    assert FLOAT32.is_integer is False


# ----------------------------------------------------------------------
# Description
# ----------------------------------------------------------------------


def test_integer_description_signed() -> None:

    assert INT32.description == (
        "int32 (4 bytes signed)"
    )


def test_integer_description_unsigned() -> None:

    assert UINT32.description == (
        "uint32 (4 bytes unsigned)"
    )


def test_float_description() -> None:

    assert FLOAT32.description == (
        "float32 (4 bytes float)"
    )


# ----------------------------------------------------------------------
# Standard integer types
# ----------------------------------------------------------------------


def test_int16_definition() -> None:

    assert INT16.name == "int16"
    assert INT16.struct_format == "h"
    assert INT16.size == 2
    assert INT16.signed is True


def test_uint16_definition() -> None:

    assert UINT16.name == "uint16"
    assert UINT16.struct_format == "H"
    assert UINT16.size == 2
    assert UINT16.signed is False


def test_int32_definition() -> None:

    assert INT32.name == "int32"
    assert INT32.struct_format == "i"
    assert INT32.size == 4
    assert INT32.signed is True


def test_uint32_definition() -> None:

    assert UINT32.name == "uint32"
    assert UINT32.struct_format == "I"
    assert UINT32.size == 4
    assert UINT32.signed is False


def test_int64_definition() -> None:

    assert INT64.name == "int64"
    assert INT64.struct_format == "q"
    assert INT64.size == 8
    assert INT64.signed is True


def test_uint64_definition() -> None:

    assert UINT64.name == "uint64"
    assert UINT64.struct_format == "Q"
    assert UINT64.size == 8
    assert UINT64.signed is False


# ----------------------------------------------------------------------
# Standard float types
# ----------------------------------------------------------------------


def test_float32_definition() -> None:

    assert FLOAT32.name == "float32"
    assert FLOAT32.struct_format == "f"
    assert FLOAT32.size == 4
    assert FLOAT32.floating is True


def test_float64_definition() -> None:

    assert FLOAT64.name == "float64"
    assert FLOAT64.struct_format == "d"
    assert FLOAT64.size == 8
    assert FLOAT64.floating is True


# ----------------------------------------------------------------------
# Collection
# ----------------------------------------------------------------------


def test_numeric_types_count() -> None:

    assert len(NUMERIC_TYPES) == 8


def test_numeric_types_contains_all_types() -> None:

    assert INT16 in NUMERIC_TYPES
    assert UINT16 in NUMERIC_TYPES
    assert INT32 in NUMERIC_TYPES
    assert UINT32 in NUMERIC_TYPES
    assert INT64 in NUMERIC_TYPES
    assert UINT64 in NUMERIC_TYPES
    assert FLOAT32 in NUMERIC_TYPES
    assert FLOAT64 in NUMERIC_TYPES


def test_numeric_type_names_unique() -> None:

    names = {
        numeric_type.name
        for numeric_type in NUMERIC_TYPES
    }

    assert len(names) == len(NUMERIC_TYPES)


def test_numeric_type_sizes_valid() -> None:

    assert all(
        numeric_type.size > 0
        for numeric_type in NUMERIC_TYPES
    )


# ----------------------------------------------------------------------
# Dataclass behaviour
# ----------------------------------------------------------------------


def test_numeric_type_is_frozen() -> None:

    with pytest.raises(
        AttributeError
    ):

        INT32.name = "changed"


def test_numeric_type_hashable() -> None:

    values = {
        INT16,
        UINT16,
        INT32,
    }

    assert len(values) == 3