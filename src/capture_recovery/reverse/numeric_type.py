"""
capture_recovery.reverse.numeric_type

Definitions of numeric types used by NumericDetector.

This module only describes numeric formats.
It does not decode binary data.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class NumericType:
    """
    Description of a binary numeric type.

    Attributes
    ----------
    name:
        Public name of the type.

    struct_format:
        Python struct module format character.

    size:
        Size in bytes.

    floating:
        True for floating point values.

    signed:
        True for signed integers.
        None for floating point values.
    """

    name: str

    struct_format: str

    size: int

    floating: bool

    signed: bool | None = None


    def __post_init__(self) -> None:
        """
        Validate numeric type definition.
        """

        if not self.name:
            raise ValueError(
                "name cannot be empty"
            )

        if not self.struct_format:
            raise ValueError(
                "struct_format cannot be empty"
            )

        if self.size <= 0:
            raise ValueError(
                "size must be > 0"
            )

        if self.floating and self.signed is not None:
            raise ValueError(
                "floating types cannot define signedness"
            )


    @property
    def is_integer(self) -> bool:
        """
        Return True for integer types.
        """

        return not self.floating


    @property
    def is_float(self) -> bool:
        """
        Return True for floating types.
        """

        return self.floating


    @property
    def description(self) -> str:
        """
        Human-readable description.
        """

        if self.floating:
            return (
                f"{self.name} "
                f"({self.size} bytes float)"
            )

        sign = (
            "signed"
            if self.signed
            else "unsigned"
        )

        return (
            f"{self.name} "
            f"({self.size} bytes {sign})"
        )


# ----------------------------------------------------------------------
# Standard numeric types
# ----------------------------------------------------------------------


INT16 = NumericType(
    name="int16",
    struct_format="h",
    size=2,
    floating=False,
    signed=True,
)


UINT16 = NumericType(
    name="uint16",
    struct_format="H",
    size=2,
    floating=False,
    signed=False,
)


INT32 = NumericType(
    name="int32",
    struct_format="i",
    size=4,
    floating=False,
    signed=True,
)


UINT32 = NumericType(
    name="uint32",
    struct_format="I",
    size=4,
    floating=False,
    signed=False,
)


INT64 = NumericType(
    name="int64",
    struct_format="q",
    size=8,
    floating=False,
    signed=True,
)


UINT64 = NumericType(
    name="uint64",
    struct_format="Q",
    size=8,
    floating=False,
    signed=False,
)


FLOAT32 = NumericType(
    name="float32",
    struct_format="f",
    size=4,
    floating=True,
)


FLOAT64 = NumericType(
    name="float64",
    struct_format="d",
    size=8,
    floating=True,
)


NUMERIC_TYPES = (
    INT16,
    UINT16,
    INT32,
    UINT32,
    INT64,
    UINT64,
    FLOAT32,
    FLOAT64,
)


__all__ = [
    "NumericType",
    "INT16",
    "UINT16",
    "INT32",
    "UINT32",
    "INT64",
    "UINT64",
    "FLOAT32",
    "FLOAT64",
    "NUMERIC_TYPES",
]