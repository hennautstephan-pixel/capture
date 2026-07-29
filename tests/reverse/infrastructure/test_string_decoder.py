"""
Tests for capture_recovery.reverse.string_decoder.
"""

from __future__ import annotations


from capture_recovery.reverse.string_decoder import (
    StringDecoder,
)

from capture_recovery.reverse.string_type import (
    ASCII,
    UTF8,
    UTF16_BE,
    UTF16_LE,
)



# ----------------------------------------------------------------------
# ASCII
# ----------------------------------------------------------------------


def test_decode_ascii() -> None:

    result = StringDecoder.decode(
        b"Hello\x00",
        0,
        ASCII,
    )


    assert result is not None
    assert result.value == "Hello"
    assert result.terminated is True



def test_decode_ascii_without_terminator() -> None:

    result = StringDecoder.decode(
        b"Hello",
        0,
        ASCII,
    )


    assert result is not None
    assert result.value == "Hello"
    assert result.terminated is False



# ----------------------------------------------------------------------
# UTF8
# ----------------------------------------------------------------------


def test_decode_utf8() -> None:

    data = "éclair".encode(
        "utf-8"
    )


    result = StringDecoder.decode(
        data,
        0,
        UTF8,
    )


    assert result is not None
    assert result.value == "éclair"



# ----------------------------------------------------------------------
# UTF16
# ----------------------------------------------------------------------


def test_decode_utf16_le() -> None:

    data = (
        "Hello"
        .encode("utf-16-le")
        +
        b"\x00\x00"
    )


    result = StringDecoder.decode(
        data,
        0,
        UTF16_LE,
    )


    assert result is not None
    assert result.value == "Hello"
    assert result.terminated is True



def test_decode_utf16_be() -> None:

    data = (
        "Hello"
        .encode("utf-16-be")
        +
        b"\x00\x00"
    )


    result = StringDecoder.decode(
        data,
        0,
        UTF16_BE,
    )


    assert result is not None
    assert result.value == "Hello"



# ----------------------------------------------------------------------
# Offset
# ----------------------------------------------------------------------


def test_decode_with_offset() -> None:

    data = (
        b"\xff\xff"
        +
        b"Test\x00"
    )


    result = StringDecoder.decode(
        data,
        2,
        ASCII,
    )


    assert result is not None
    assert result.offset == 2
    assert result.value == "Test"



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_decode_invalid_offset() -> None:

    result = StringDecoder.decode(
        b"abc",
        99,
        ASCII,
    )


    assert result is None



def test_can_decode_ascii() -> None:

    assert StringDecoder.can_decode(
        b"Hello",
        0,
        ASCII,
    )



def test_can_decode_utf8() -> None:

    assert StringDecoder.can_decode(
        "é".encode("utf-8"),
        0,
        UTF8,
    )