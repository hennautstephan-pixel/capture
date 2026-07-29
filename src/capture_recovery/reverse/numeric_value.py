"""
capture_recovery.reverse.numeric_value

Representation of decoded numeric values.
"""

from __future__ import annotations

from dataclasses import dataclass

from .numeric_type import (
    FLOAT32,
    FLOAT64,
    INT16,
    INT32,
    INT64,
    UINT16,
    UINT32,
    UINT64,
    NumericType,
)


_TYPE_MAP = {
    item.name: item
    for item in (
        INT16,
        UINT16,
        INT32,
        UINT32,
        INT64,
        UINT64,
        FLOAT32,
        FLOAT64,
    )
}


@dataclass(
    slots=True,
    frozen=True,
    init=False,
)
class NumericValue:
    """
    Decoded numeric value.

    Compatible with V1 and V2 constructors.
    """

    offset: int

    numeric_type: NumericType

    endianness: str

    value: int | float


    def __init__(
        self,
        *,
        offset: int,
        value: int | float,
        endianness: str,
        numeric_type: NumericType | None = None,
        type_name: str | None = None,
        size: int | None = None,
    ) -> None:

        if numeric_type is None:

            if type_name is None:
                raise ValueError(
                    "numeric_type or type_name required"
                )

            try:
                numeric_type = _TYPE_MAP[type_name]

            except KeyError:
                raise ValueError(
                    f"unknown numeric type: {type_name}"
                )

        if offset < 0:
            raise ValueError(
                "offset must be >= 0"
            )

        if endianness not in {
            "little",
            "big",
        }:
            raise ValueError(
                "invalid endianness"
            )

        if size is not None:
            if size != numeric_type.size:
                raise ValueError(
                    "size mismatch"
                )

        object.__setattr__(
            self,
            "offset",
            offset,
        )

        object.__setattr__(
            self,
            "numeric_type",
            numeric_type,
        )

        object.__setattr__(
            self,
            "endianness",
            endianness,
        )

        object.__setattr__(
            self,
            "value",
            value,
        )


    @property
    def type_name(self) -> str:
        """
        Compatibility property.
        """

        return self.numeric_type.name


    @property
    def size(self) -> int:
        """
        Size in bytes.
        """

        return self.numeric_type.size


    @property
    def is_float(self) -> bool:
        return self.numeric_type.is_float


    @property
    def is_integer(self) -> bool:
        return self.numeric_type.is_integer


    @property
    def endianness_prefix(self) -> str:

        return (
            "<"
            if self.endianness == "little"
            else ">"
        )


    def as_dict(self) -> dict[str, object]:

        return {
            "offset": self.offset,
            "type": self.type_name,
            "size": self.size,
            "endianness": self.endianness,
            "value": self.value,
        }