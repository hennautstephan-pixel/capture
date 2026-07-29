"""
Tests for capture_recovery.reverse.numeric_detector
"""

from __future__ import annotations

import math
import struct

from capture_recovery.reverse.numeric_detector import (
    NumericDetector,
    NumericValue,
)


# ----------------------------------------------------------------------
# Basic API
# ----------------------------------------------------------------------


def test_empty_buffer():
    assert NumericDetector.detect(b"") == []


def test_bytes_supported():
    values = NumericDetector.detect(
        b"\x01\x00"
    )

    assert values


def test_bytearray_supported():
    values = NumericDetector.detect(
        bytearray(b"\x01\x00")
    )

    assert values


def test_memoryview_supported():
    values = NumericDetector.detect(
        memoryview(b"\x01\x00")
    )

    assert values


def test_detect_returns_list():
    values = NumericDetector.detect(
        b"\x01\x00"
    )

    assert isinstance(values, list)


def test_detect_returns_new_list():
    a = NumericDetector.detect(
        b"\x01\x00"
    )

    b = NumericDetector.detect(
        b"\x01\x00"
    )

    assert a is not b


# ----------------------------------------------------------------------
# NumericValue
# ----------------------------------------------------------------------


def test_numericvalue_integer_property():

    value = NumericValue(
        offset=0,
        type_name="uint32",
        endianness="little",
        size=4,
        value=123,
    )

    assert value.is_integer
    assert not value.is_float


def test_numericvalue_float_property():

    value = NumericValue(
        offset=0,
        type_name="float32",
        endianness="little",
        size=4,
        value=1.5,
    )

    assert value.is_float
    assert not value.is_integer


def test_numericvalue_hashable():

    value = NumericValue(
        offset=0,
        type_name="uint16",
        endianness="little",
        size=2,
        value=15,
    )

    assert hash(value)


# ----------------------------------------------------------------------
# Integer decoding
# ----------------------------------------------------------------------


def test_detect_uint16_little():

    data = struct.pack(
        "<H",
        1234,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "uint16"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert len(result) == 1
    assert result[0].value == 1234


def test_detect_uint16_big():

    data = struct.pack(
        ">H",
        1234,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "uint16"
        and value.endianness == "big"
        and value.offset == 0
    ]

    assert len(result) == 1
    assert result[0].value == 1234


def test_detect_int16():

    number = -1234

    data = struct.pack(
        "<h",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "int16"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert result[0].value == number


def test_detect_uint32():

    number = 987654321

    data = struct.pack(
        "<I",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "uint32"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert result[0].value == number


def test_detect_int32():

    number = -654321

    data = struct.pack(
        "<i",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "int32"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert result[0].value == number


def test_detect_uint64():

    number = 123456789012345

    data = struct.pack(
        "<Q",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "uint64"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert result[0].value == number


def test_detect_int64():

    number = -123456789012345

    data = struct.pack(
        "<q",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "int64"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert result[0].value == number

# ----------------------------------------------------------------------
# Floating point decoding
# ----------------------------------------------------------------------


def test_detect_float32():

    number = 12.5

    data = struct.pack(
        "<f",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "float32"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert len(result) == 1

    assert math.isclose(
        result[0].value,
        number,
    )


def test_detect_float64():

    number = 123456.789

    data = struct.pack(
        "<d",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "float64"
        and value.endianness == "little"
        and value.offset == 0
    ]

    assert len(result) == 1

    assert math.isclose(
        result[0].value,
        number,
    )


def test_detect_big_endian_float32():

    number = 8.75

    data = struct.pack(
        ">f",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "float32"
        and value.endianness == "big"
        and value.offset == 0
    ]

    assert len(result) == 1

    assert math.isclose(
        result[0].value,
        number,
    )


def test_detect_big_endian_float64():

    number = 98765.4321

    data = struct.pack(
        ">d",
        number,
    )

    values = NumericDetector.detect(data)

    result = [
        value
        for value in values
        if value.type_name == "float64"
        and value.endianness == "big"
        and value.offset == 0
    ]

    assert len(result) == 1

    assert math.isclose(
        result[0].value,
        number,
    )


# ----------------------------------------------------------------------
# Detector options
# ----------------------------------------------------------------------


def test_disable_floats():

    data = struct.pack(
        "<f",
        1.0,
    )

    values = NumericDetector.detect(
        data,
        floats=False,
    )

    assert values

    assert all(
        value.is_integer
        for value in values
    )


def test_disable_integers():

    data = struct.pack(
        "<I",
        123,
    )

    values = NumericDetector.detect(
        data,
        integers=False,
    )

    assert values

    assert all(
        value.is_float
        for value in values
    )


# ----------------------------------------------------------------------
# Helper methods
# ----------------------------------------------------------------------


def test_filter_integers():

    values = NumericDetector.detect(
        struct.pack(
            "<If",
            5,
            2.5,
        )
    )

    integers = NumericDetector.integers(values)

    assert integers

    assert all(
        value.is_integer
        for value in integers
    )


def test_filter_floats():

    values = NumericDetector.detect(
        struct.pack(
            "<If",
            5,
            2.5,
        )
    )

    floats = NumericDetector.floats(values)

    assert floats

    assert all(
        value.is_float
        for value in floats
    )


def test_filter_by_type():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            100,
        )
    )

    selected = NumericDetector.by_type(
        values,
        "uint32",
    )

    assert selected

    assert all(
        value.type_name == "uint32"
        for value in selected
    )


def test_filter_by_offset():

    data = (
        struct.pack("<H", 1)
        + struct.pack("<H", 2)
    )

    values = NumericDetector.detect(data)

    selected = NumericDetector.by_offset(
        values,
        2,
    )

    assert selected

    assert all(
        value.offset == 2
        for value in selected
    )


def test_filter_range():

    values = NumericDetector.detect(
        struct.pack(
            "<III",
            1,
            100,
            1000,
        )
    )

    selected = NumericDetector.range(
        values,
        minimum=50,
        maximum=200,
    )

    assert selected

    assert all(
        50 <= value.value <= 200
        for value in selected
    )    

# ----------------------------------------------------------------------
# NaN / Infinity handling
# ----------------------------------------------------------------------


def test_nan_filtered():

    data = struct.pack(
        "<f",
        float("nan"),
    )

    values = NumericDetector.detect(data)

    assert not any(
        value.type_name == "float32"
        and value.endianness == "little"
        and value.offset == 0
        for value in values
    )


def test_nan_not_filtered():

    data = struct.pack(
        "<f",
        float("nan"),
    )

    values = NumericDetector.detect(
        data,
        finite_only=False,
    )

    assert any(
        value.type_name == "float32"
        and value.endianness == "little"
        and value.offset == 0
        for value in values
    )


def test_infinite_filtered():

    data = struct.pack(
        "<f",
        float("inf"),
    )

    values = NumericDetector.detect(data)

    assert not any(
        value.type_name == "float32"
        and value.endianness == "little"
        and value.offset == 0
        for value in values
    )


def test_infinite_not_filtered():

    data = struct.pack(
        "<f",
        float("inf"),
    )

    values = NumericDetector.detect(
        data,
        finite_only=False,
    )

    assert any(
        value.type_name == "float32"
        and value.endianness == "little"
        and value.offset == 0
        for value in values
    )


# ----------------------------------------------------------------------
# Multiple offsets
# ----------------------------------------------------------------------


def test_multiple_offsets_uint16():

    data = (
        struct.pack("<H", 10)
        + struct.pack("<H", 20)
        + struct.pack("<H", 30)
    )

    values = NumericDetector.detect(data)

    offsets = {
        value.offset
        for value in values
        if value.type_name == "uint16"
        and value.endianness == "little"
    }

    assert 0 in offsets
    assert 2 in offsets
    assert 4 in offsets


def test_multiple_offsets_float32():

    data = (
        struct.pack("<f", 1.5)
        + struct.pack("<f", 2.5)
    )

    values = NumericDetector.detect(data)

    offsets = {
        value.offset
        for value in values
        if value.type_name == "float32"
        and value.endianness == "little"
    }

    assert {0, 4}.issubset(offsets)


def test_partial_buffer_does_not_crash():

    values = NumericDetector.detect(
        b"\x01"
    )

    assert isinstance(
        values,
        list,
    )


def test_detect_single_byte():

    values = NumericDetector.detect(
        b"\xFF"
    )

    assert isinstance(
        values,
        list,
    )


def test_detect_three_bytes():

    values = NumericDetector.detect(
        b"\x01\x02\x03"
    )

    assert isinstance(
        values,
        list,
    )


# ----------------------------------------------------------------------
# Range helper
# ----------------------------------------------------------------------


def test_empty_range_result():

    values = NumericDetector.detect(
        struct.pack(
            "<III",
            1,
            2,
            3,
        )
    )

    selected = NumericDetector.range(
        values,
        minimum=100,
        maximum=200,
    )

    assert selected == []


def test_by_type_unknown():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            10,
        )
    )

    selected = NumericDetector.by_type(
        values,
        "foobar",
    )

    assert selected == []


def test_by_offset_unknown():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            10,
        )
    )

    selected = NumericDetector.by_offset(
        values,
        999,
    )

    assert selected == []


def test_integer_helper_empty():

    assert NumericDetector.integers([]) == []


def test_float_helper_empty():

    assert NumericDetector.floats([]) == []

# ----------------------------------------------------------------------
# Consistency
# ----------------------------------------------------------------------


def test_detect_result_contains_numericvalue():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            42,
        )
    )

    assert values

    assert all(
        isinstance(value, NumericValue)
        for value in values
    )


def test_detect_result_offsets_are_valid():

    data = struct.pack(
        "<II",
        1,
        2,
    )

    values = NumericDetector.detect(data)

    assert all(
        0 <= value.offset < len(data)
        for value in values
    )


def test_detect_result_sizes_are_valid():

    values = NumericDetector.detect(
        struct.pack(
            "<Q",
            123456,
        )
    )

    valid_sizes = {2, 4, 8}

    assert all(
        value.size in valid_sizes
        for value in values
    )


def test_detect_result_endianness():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            10,
        )
    )

    assert all(
        value.endianness in (
            "little",
            "big",
        )
        for value in values
    )


def test_detect_result_type_names():

    valid = {
        "int16",
        "uint16",
        "int32",
        "uint32",
        "int64",
        "uint64",
        "float32",
        "float64",
    }

    values = NumericDetector.detect(
        struct.pack(
            "<Q",
            1,
        )
    )

    assert all(
        value.type_name in valid
        for value in values
    )


# ----------------------------------------------------------------------
# Boundary values
# ----------------------------------------------------------------------


def test_zero_value():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            0,
        )
    )

    assert any(
        value.value == 0
        and value.type_name == "uint32"
        and value.endianness == "little"
        for value in values
    )


def test_negative_integer():

    number = -1

    values = NumericDetector.detect(
        struct.pack(
            "<i",
            number,
        )
    )

    assert any(
        value.value == number
        and value.type_name == "int32"
        and value.endianness == "little"
        for value in values
    )


def test_large_unsigned_integer():

    number = 0xFFFFFFFFFFFFFFFF

    values = NumericDetector.detect(
        struct.pack(
            "<Q",
            number,
        )
    )

    assert any(
        value.value == number
        and value.type_name == "uint64"
        and value.endianness == "little"
        for value in values
    )


def test_small_float():

    number = 0.000001

    values = NumericDetector.detect(
        struct.pack(
            "<f",
            number,
        )
    )

    assert any(
        value.type_name == "float32"
        and value.endianness == "little"
        and math.isclose(
            value.value,
            number,
            rel_tol=1e-6,
        )
        for value in values
    )


def test_large_float64():

    number = 1.23456789012345e100

    values = NumericDetector.detect(
        struct.pack(
            "<d",
            number,
        )
    )

    assert any(
        value.type_name == "float64"
        and value.endianness == "little"
        and math.isclose(
            value.value,
            number,
            rel_tol=1e-12,
        )
        for value in values
    )


# ----------------------------------------------------------------------
# Regression tests
# ----------------------------------------------------------------------


def test_detect_is_repeatable():

    data = struct.pack(
        "<II",
        100,
        200,
    )

    first = NumericDetector.detect(data)
    second = NumericDetector.detect(data)

    assert first == second


def test_helper_methods_do_not_modify_input():

    values = NumericDetector.detect(
        struct.pack(
            "<If",
            10,
            2.5,
        )
    )

    original = list(values)

    NumericDetector.integers(values)
    NumericDetector.floats(values)
    NumericDetector.by_type(values, "uint32")
    NumericDetector.by_offset(values, 0)
    NumericDetector.range(
        values,
        minimum=0,
        maximum=100,
    )

    assert values == original


def test_detect_non_empty_buffer_returns_values():

    values = NumericDetector.detect(
        struct.pack(
            "<I",
            123,
        )
    )

    assert len(values) > 0


def test_detect_large_buffer():

    data = bytes(range(256))

    values = NumericDetector.detect(data)

    assert isinstance(values, list)
    assert len(values) > 0


def test_detect_with_all_options_enabled():

    values = NumericDetector.detect(
        struct.pack(
            "<If",
            1,
            2.5,
        ),
        integers=True,
        floats=True,
        finite_only=True,
    )

    assert values


def test_detect_without_filters():

    values = NumericDetector.detect(
        struct.pack(
            "<If",
            1,
            2.5,
        ),
        finite_only=False,
    )

    assert values


def test_detect_returns_only_numericvalue_instances():

    values = NumericDetector.detect(
        bytes(range(32))
    )

    assert all(
        isinstance(value, NumericValue)
        for value in values
    )