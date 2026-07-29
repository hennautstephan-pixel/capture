"""
Tests for capture_recovery.reverse.guid_decoder.
"""

from __future__ import annotations


from capture_recovery.reverse.guid_decoder import (
    GuidDecoder,
)

from capture_recovery.reverse.guid_type import (
    RFC4122_UUID,
    WINDOWS_GUID,
)



# ----------------------------------------------------------------------
# Windows GUID
# ----------------------------------------------------------------------


def test_decode_windows_guid() -> None:

    data = bytes.fromhex(
        "78563412"
        "3412"
        "cdab"
        "ef0123456789abcd"
    )


    result = GuidDecoder.decode(
        data,
        0,
        WINDOWS_GUID,
    )


    assert result is not None

    assert (
        result.value
        ==
        "12345678-1234-abcd-ef01-23456789abcd"
    )



def test_windows_raw_bytes_kept() -> None:

    data = bytes.fromhex(
        "78563412"
        "3412"
        "cdab"
        "ef0123456789abcd"
    )


    result = GuidDecoder.decode(
        data,
        0,
        WINDOWS_GUID,
    )


    assert result.raw_bytes == data



# ----------------------------------------------------------------------
# RFC UUID
# ----------------------------------------------------------------------


def test_decode_rfc_uuid() -> None:

    data = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )


    result = GuidDecoder.decode(
        data,
        0,
        RFC4122_UUID,
    )


    assert result is not None

    assert (
        result.value
        ==
        "00112233-4455-6677-8899-aabbccddeeff"
    )



# ----------------------------------------------------------------------
# Offset
# ----------------------------------------------------------------------


def test_decode_with_offset() -> None:

    guid = bytes.fromhex(
        "785634123412cdab"
        "ef0123456789abcd"
    )


    data = (
        b"\xff\xff"
        +
        guid
    )


    result = GuidDecoder.decode(
        data,
        2,
        WINDOWS_GUID,
    )


    assert result.offset == 2



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_can_decode_valid() -> None:

    assert GuidDecoder.can_decode(
        bytes(16),
        0,
        WINDOWS_GUID,
    )



def test_can_decode_invalid_offset() -> None:

    assert not GuidDecoder.can_decode(
        bytes(10),
        0,
        WINDOWS_GUID,
    )



def test_decode_too_short_returns_none() -> None:

    result = GuidDecoder.decode(
        bytes(4),
        0,
        WINDOWS_GUID,
    )


    assert result is None