"""
Tests for capture_recovery.reverse.numeric_value.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.numeric_type import (
    FLOAT32,
    INT32,
    UINT64,
)

from capture_recovery.reverse.numeric_value import (
    NumericValue,
)


# ----------------------------------------------------------------------
# Creation
# ----------------------------------------------------------------------


def test_create_integer_value() -> None:

    value = NumericValue(
        offset=10,
        numeric_type=INT32,
        endianness="little",
        value=-42,
    )

    assert value.offset == 10
    assert value.value == -42


def test_create_float_value() -> None:

    value = NumericValue(
        offset=4,
        numeric_type=FLOAT32,
        endianness="big",
        value=1.5,
    )

    assert value.value == 1.5


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_negative_offset_rejected() -> None:

    with pytest.raises(ValueError):

        NumericValue(
            offset=-1,
            numeric_type=INT32,
            endianness="little",
            value=1,
        )


def test_invalid_endianness_rejected() -> None:

    with pytest.raises(ValueError):

        NumericValue(
            offset=0,
            numeric_type=INT32,
            endianness="middle",
            value=1,
        )


# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_size_property() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=UINT64,
        endianness="little",
        value=100,
    )

    assert value.size == 8


def test_type_name_property() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="little",
        value=100,
    )

    assert value.type_name == "int32"


def test_integer_property() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="little",
        value=10,
    )

    assert value.is_integer is True
    assert value.is_float is False


def test_float_property() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=FLOAT32,
        endianness="little",
        value=10.5,
    )

    assert value.is_float is True
    assert value.is_integer is False


# ----------------------------------------------------------------------
# Endianness
# ----------------------------------------------------------------------


def test_little_endian_prefix() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="little",
        value=1,
    )

    assert value.endianness_prefix == "<"


def test_big_endian_prefix() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="big",
        value=1,
    )

    assert value.endianness_prefix == ">"


# ----------------------------------------------------------------------
# Serialization
# ----------------------------------------------------------------------


def test_as_dict() -> None:

    value = NumericValue(
        offset=20,
        numeric_type=FLOAT32,
        endianness="little",
        value=2.5,
    )

    result = value.as_dict()

    assert result == {
        "offset": 20,
        "type": "float32",
        "size": 4,
        "endianness": "little",
        "value": 2.5,
    }


# ----------------------------------------------------------------------
# Dataclass behaviour
# ----------------------------------------------------------------------


def test_frozen() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="little",
        value=1,
    )

    with pytest.raises(AttributeError):

        value.value = 2


def test_hashable() -> None:

    value = NumericValue(
        offset=0,
        numeric_type=INT32,
        endianness="little",
        value=1,
    )

    assert hash(value)