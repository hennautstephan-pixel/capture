import struct
import uuid

import pytest

from capture_recovery.parser.binary_stream import BinaryStream


def test_size_position_remaining():
    stream = BinaryStream(b"\x01\x02\x03")

    assert stream.size == 3
    assert stream.position == 0
    assert stream.remaining == 3


def test_read_u8():
    stream = BinaryStream(b"\x12")

    assert stream.u8() == 0x12
    assert stream.eof()


def test_read_u16():
    stream = BinaryStream(b"\x34\x12")

    assert stream.u16() == 0x1234


def test_read_u32():
    stream = BinaryStream(b"\x78\x56\x34\x12")

    assert stream.u32() == 0x12345678


def test_read_u64():
    value = 0x1122334455667788
    stream = BinaryStream(struct.pack("<Q", value))

    assert stream.u64() == value


def test_read_i32():
    value = -123456

    stream = BinaryStream(struct.pack("<i", value))

    assert stream.i32() == value


def test_read_float():
    value = 123.5

    stream = BinaryStream(struct.pack("<f", value))

    assert stream.f32() == pytest.approx(value)


def test_read_double():
    value = 9876.125

    stream = BinaryStream(struct.pack("<d", value))

    assert stream.f64() == pytest.approx(value)


def test_uuid():
    u = uuid.uuid4()

    stream = BinaryStream(u.bytes_le)

    assert stream.uuid() == u


def test_peek():
    stream = BinaryStream(b"\x01\x02\x03")

    assert stream.peek(2) == b"\x01\x02"
    assert stream.position == 0


def test_seek_skip():
    stream = BinaryStream(b"\x01\x02\x03\x04")

    stream.seek(1)

    assert stream.tell() == 1

    stream.skip(2)

    assert stream.tell() == 3

    assert stream.u8() == 4


def test_cstring():
    stream = BinaryStream(b"Capture\x00AAAA")

    assert stream.cstring() == "Capture"

    assert stream.tell() == 8


def test_fixed_string():
    stream = BinaryStream(b"HelloWorld")

    assert stream.fixed_string(5) == "Hello"


def test_slice():
    stream = BinaryStream(b"\x01\x02\x03\x04\x05")

    assert stream.slice(1, 3) == b"\x02\x03\x04"


def test_align():
    stream = BinaryStream(b"\x00" * 32)

    stream.seek(3)

    stream.align(4)

    assert stream.tell() == 4

    stream.seek(5)

    stream.align(8)

    assert stream.tell() == 8


def test_read_past_end():
    stream = BinaryStream(b"\x01")

    stream.u8()

    with pytest.raises(EOFError):
        stream.u8()


def test_invalid_seek():
    stream = BinaryStream(b"\x01")

    with pytest.raises(ValueError):
        stream.seek(-1)


def test_invalid_slice():
    stream = BinaryStream(b"\x01\x02")

    with pytest.raises(EOFError):
        stream.slice(1, 4)