"""
capture_recovery.reverse.guid_type

Definitions of supported GUID formats.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class GuidType:
    """
    Description of a GUID binary format.

    Attributes
    ----------
    name:
        Public identifier.

    size:
        Binary size in bytes.

    microsoft_order:
        True for Windows GUID byte ordering.
    """

    name: str

    size: int = 16

    microsoft_order: bool = True


    def __post_init__(self) -> None:
        """
        Validate definition.
        """

        if not self.name:
            raise ValueError(
                "name cannot be empty"
            )


        if self.size != 16:
            raise ValueError(
                "GUID size must be 16 bytes"
            )


    @property
    def is_windows(self) -> bool:
        """
        Return True for Microsoft GUID layout.
        """

        return self.microsoft_order


    @property
    def is_rfc4122(self) -> bool:
        """
        Return True for standard UUID layout.
        """

        return not self.microsoft_order



# ----------------------------------------------------------------------
# Standard formats
# ----------------------------------------------------------------------


WINDOWS_GUID = GuidType(
    name="windows_guid",
    size=16,
    microsoft_order=True,
)


RFC4122_UUID = GuidType(
    name="rfc4122_uuid",
    size=16,
    microsoft_order=False,
)


GUID_TYPES = (
    WINDOWS_GUID,
    RFC4122_UUID,
)


__all__ = [
    "GuidType",
    "WINDOWS_GUID",
    "RFC4122_UUID",
    "GUID_TYPES",
]