"""
Tests for capture_recovery.reverse.hex_inspector
"""

from __future__ import annotations

import math
import struct

import pytest

from capture_recovery.reverse.hex_inspector import (
    HexInspector,
    HexRow,
)


def test_empty_buffer_returns_empty_list():
    rows = HexInspector.inspect(b"")

    assert rows == []


def test_returns_hexrow_instances():
    rows = HexInspector.inspect(b"abcd")

    assert len(rows) == 1
    assert isinstance(rows[0], HexRow)


def test_default_width_is_16():
    data = bytes(range(32))

    rows = HexInspector.inspect(data)

    assert len(rows) == 2
    assert rows[0].offset == 0
    assert rows[1].offset == 16


def test_custom_width():
    data = bytes(range(20))

    rows = HexInspector.inspect(data, width=8)

    assert len(rows) == 3

    assert rows[0].offset == 0
    assert rows[1].offset == 8
    assert rows[2].offset == 16


def test_invalid_width_raises():
    with pytest.raises(ValueError):
        HexInspector.inspect(b"abc", width=0)

    with pytest.raises(ValueError):
        HexInspector.inspect(b"abc", width=-1)


def test_hex_output():
    rows = HexInspector.inspect(bytes([0x00, 0x01, 0xAB, 0xFF]))

    assert rows[0].hex == "00 01 AB FF"


def test_ascii_output():
    rows = HexInspector.inspect(b"ABC\x00xyz")

    assert rows[0].ascii == "ABC.xyz"


def test_non_printable_are_replaced():
    rows = HexInspector.inspect(bytes([1, 2, 3, 65, 66, 67]))

    assert rows[0].ascii == "...ABC"


def test_u32_little_endian():
    value = 123456789

    rows = HexInspector.inspect(struct.pack("<I", value))

    assert rows[0].u32_le == value


def test_f32_little_endian():
    value = 1.5

    rows = HexInspector.inspect(struct.pack("<f", value))

    assert math.isclose(
        rows[0].f32_le,
        value,
        rel_tol=1e-6,
    )


def test_less_than_four_bytes():
    rows = HexInspector.inspect(b"\x01\x02\x03")

    assert rows[0].u32_le is None
    assert rows[0].f32_le is None


def test_raw_bytes_preserved():
    data = b"Hello"

    rows = HexInspector.inspect(data)

    assert rows[0].raw == data


def test_memoryview_supported():
    data = memoryview(b"abcdef")

    rows = HexInspector.inspect(data)

    assert rows[0].raw == b"abcdef"


def test_bytearray_supported():
    data = bytearray(b"abcdef")

    rows = HexInspector.inspect(data)

    assert rows[0].raw == b"abcdef"


def test_last_partial_row():
    data = bytes(range(18))

    rows = HexInspector.inspect(data)

    assert len(rows) == 2
    assert rows[1].raw == bytes([16, 17])


def test_offsets_are_correct():
    data = bytes(range(64))

    rows = HexInspector.inspect(data)

    assert [row.offset for row in rows] == [0, 16, 32, 48]