"""
capture_recovery.reverse.string_type

Definitions of supported string encodings.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class StringType:
    """
    Description of a binary string encoding.

    Attributes
    ----------
    name:
        Public identifier.

    encoding:
        Python codec name.

    char_width:
        Number of bytes per character.

    null_terminated:
        Whether strings normally end with NULL.
    """

    name: str

    encoding: str

    char_width: int

    null_terminated: bool = True


    def __post_init__(self) -> None:
        """
        Validate definition.
        """

        if not self.name:
            raise ValueError(
                "name cannot be empty"
            )

        if not self.encoding:
            raise ValueError(
                "encoding cannot be empty"
            )

        if self.char_width <= 0:
            raise ValueError(
                "char_width must be > 0"
            )


    @property
    def is_single_byte(self) -> bool:
        """
        Return True for one byte characters.
        """

        return self.char_width == 1


    @property
    def is_wide(self) -> bool:
        """
        Return True for multi-byte characters.
        """

        return self.char_width > 1



# ----------------------------------------------------------------------
# Standard string types
# ----------------------------------------------------------------------


ASCII = StringType(
    name="ascii",
    encoding="ascii",
    char_width=1,
)


UTF8 = StringType(
    name="utf8",
    encoding="utf-8",
    char_width=1,
)


UTF16_LE = StringType(
    name="utf16_le",
    encoding="utf-16-le",
    char_width=2,
)


UTF16_BE = StringType(
    name="utf16_be",
    encoding="utf-16-be",
    char_width=2,
)


STRING_TYPES = (
    ASCII,
    UTF8,
    UTF16_LE,
    UTF16_BE,
)


__all__ = [
    "StringType",
    "ASCII",
    "UTF8",
    "UTF16_LE",
    "UTF16_BE",
    "STRING_TYPES",
]