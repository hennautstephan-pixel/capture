"""
capture_recovery.reverse.guid_value

Representation of decoded GUID values.
"""

from __future__ import annotations

from dataclasses import dataclass

from .guid_type import GuidType



@dataclass(
    frozen=True,
    slots=True,
)
class GuidValue:
    """
    Decoded GUID value.

    Attributes
    ----------
    offset:
        Position in binary buffer.

    guid_type:
        Detected GUID format.

    value:
        Text UUID representation.

    raw_bytes:
        Original 16 bytes.
    """

    offset: int

    guid_type: GuidType

    value: str

    raw_bytes: bytes



    def __post_init__(self) -> None:
        """
        Validate GUID value.
        """

        if self.offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )


        if len(self.raw_bytes) != 16:

            raise ValueError(
                "raw_bytes must contain 16 bytes"
            )


        if not isinstance(
            self.value,
            str,
        ):
            raise TypeError(
                "value must be str"
            )



    @property
    def length(self) -> int:
        """
        Return binary size.
        """

        return len(
            self.raw_bytes
        )



    @property
    def type_name(self) -> str:
        """
        Return GUID type name.
        """

        return self.guid_type.name



    @property
    def is_windows(self) -> bool:
        """
        True for Windows GUID layout.
        """

        return self.guid_type.is_windows



    @property
    def is_rfc4122(self) -> bool:
        """
        True for RFC UUID layout.
        """

        return self.guid_type.is_rfc4122



    def as_dict(self) -> dict[str, object]:
        """
        Convert to serializable form.
        """

        return {
            "offset": self.offset,
            "type": self.type_name,
            "value": self.value,
            "length": self.length,
            "windows": self.is_windows,
        }