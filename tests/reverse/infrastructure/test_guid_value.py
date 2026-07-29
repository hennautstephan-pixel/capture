"""
Tests for capture_recovery.reverse.guid_value.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.guid_type import (
    RFC4122_UUID,
    WINDOWS_GUID,
)

from capture_recovery.reverse.guid_value import (
    GuidValue,
)



RAW_GUID = bytes(
    range(16)
)


def create_value() -> GuidValue:

    return GuidValue(
        offset=10,
        guid_type=WINDOWS_GUID,
        value="00112233-4455-6677-8899-aabbccddeeff",
        raw_bytes=RAW_GUID,
    )



# ----------------------------------------------------------------------
# Creation
# ----------------------------------------------------------------------


def test_create_guid_value() -> None:

    value = create_value()

    assert value.offset == 10
    assert (
        value.value
        ==
        "00112233-4455-6677-8899-aabbccddeeff"
    )



def test_raw_bytes_kept() -> None:

    value = create_value()

    assert value.raw_bytes == RAW_GUID



# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_length() -> None:

    value = create_value()

    assert value.length == 16



def test_type_name() -> None:

    value = create_value()

    assert value.type_name == "windows_guid"



def test_windows_property() -> None:

    value = create_value()

    assert value.is_windows is True



def test_rfc_property() -> None:

    value = GuidValue(
        offset=0,
        guid_type=RFC4122_UUID,
        value="00112233-4455-6677-8899-aabbccddeeff",
        raw_bytes=RAW_GUID,
    )

    assert value.is_rfc4122 is True



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_negative_offset_rejected() -> None:

    with pytest.raises(ValueError):

        GuidValue(
            offset=-1,
            guid_type=WINDOWS_GUID,
            value="test",
            raw_bytes=RAW_GUID,
        )



def test_invalid_size_rejected() -> None:

    with pytest.raises(ValueError):

        GuidValue(
            offset=0,
            guid_type=WINDOWS_GUID,
            value="test",
            raw_bytes=b"abc",
        )



def test_value_type_rejected() -> None:

    with pytest.raises(TypeError):

        GuidValue(
            offset=0,
            guid_type=WINDOWS_GUID,
            value=123,
            raw_bytes=RAW_GUID,
        )



# ----------------------------------------------------------------------
# Serialization
# ----------------------------------------------------------------------


def test_as_dict() -> None:

    value = create_value()

    result = value.as_dict()

    assert result["offset"] == 10
    assert result["type"] == "windows_guid"
    assert result["length"] == 16