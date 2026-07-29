"""
capture_recovery.reverse.string_value

Representation of decoded strings.
"""

from __future__ import annotations

from dataclasses import dataclass

from .string_type import StringType


@dataclass(
    frozen=True,
    slots=True,
)
class StringValue:
    """
    Decoded string value.

    Attributes
    ----------
    offset:
        Position in binary buffer.

    string_type:
        Detected string encoding.

    value:
        Decoded text.

    raw_bytes:
        Original bytes.

    terminated:
        Whether a NULL terminator was found.
    """

    offset: int

    string_type: StringType

    value: str

    raw_bytes: bytes

    terminated: bool = False



    def __post_init__(self) -> None:
        """
        Validate value.
        """

        if self.offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )


        if not isinstance(
            self.value,
            str,
        ):
            raise TypeError(
                "value must be str"
            )


        if not isinstance(
            self.raw_bytes,
            bytes,
        ):
            raise TypeError(
                "raw_bytes must be bytes"
            )


    @property
    def length(self) -> int:
        """
        Return byte length.
        """

        return len(
            self.raw_bytes
        )


    @property
    def char_length(self) -> int:
        """
        Return number of characters.
        """

        return len(
            self.value
        )


    @property
    def type_name(self) -> str:
        """
        Return string type name.
        """

        return self.string_type.name


    @property
    def encoding(self) -> str:
        """
        Return Python encoding name.
        """

        return self.string_type.encoding


    @property
    def is_ascii(self) -> bool:
        """
        True for ASCII strings.
        """

        return (
            self.string_type.name
            == "ascii"
        )


    @property
    def is_utf8(self) -> bool:
        """
        True for UTF-8 strings.
        """

        return (
            self.string_type.name
            == "utf8"
        )


    @property
    def is_utf16(self) -> bool:
        """
        True for UTF-16 strings.
        """

        return self.string_type.is_wide



    def as_dict(self) -> dict[str, object]:
        """
        Convert to serializable dictionary.
        """

        return {
            "offset": self.offset,
            "type": self.type_name,
            "encoding": self.encoding,
            "value": self.value,
            "length": self.length,
            "terminated": self.terminated,
        }