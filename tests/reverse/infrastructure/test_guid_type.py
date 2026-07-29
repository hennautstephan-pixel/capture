"""
Tests for capture_recovery.reverse.guid_type.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.guid_type import (
    GUID_TYPES,
    RFC4122_UUID,
    WINDOWS_GUID,
    GuidType,
)



# ----------------------------------------------------------------------
# Creation
# ----------------------------------------------------------------------


def test_create_guid_type() -> None:

    value = GuidType(
        name="test",
    )

    assert value.name == "test"
    assert value.size == 16



def test_default_windows_order() -> None:

    value = GuidType(
        name="test",
    )

    assert value.microsoft_order is True



# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_empty_name_rejected() -> None:

    with pytest.raises(ValueError):

        GuidType(
            name="",
        )



def test_invalid_size_rejected() -> None:

    with pytest.raises(ValueError):

        GuidType(
            name="bad",
            size=8,
        )



# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------


def test_windows_guid_property() -> None:

    assert WINDOWS_GUID.is_windows is True



def test_rfc_uuid_property() -> None:

    assert RFC4122_UUID.is_rfc4122 is True



# ----------------------------------------------------------------------
# Standard values
# ----------------------------------------------------------------------


def test_windows_guid_definition() -> None:

    assert WINDOWS_GUID.name == "windows_guid"
    assert WINDOWS_GUID.size == 16



def test_rfc_definition() -> None:

    assert RFC4122_UUID.name == "rfc4122_uuid"
    assert RFC4122_UUID.size == 16



def test_guid_types_count() -> None:

    assert len(GUID_TYPES) == 2



def test_guid_names_unique() -> None:

    names = {
        item.name
        for item in GUID_TYPES
    }

    assert len(names) == len(
        GUID_TYPES
    )



# ----------------------------------------------------------------------
# Immutability
# ----------------------------------------------------------------------


def test_guid_type_is_frozen() -> None:

    with pytest.raises(AttributeError):

        WINDOWS_GUID.name = "changed"