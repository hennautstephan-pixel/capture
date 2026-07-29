"""
capture_recovery.reverse.numeric_decoder

Decode binary data into NumericValue objects.
"""

from __future__ import annotations

import struct

from .numeric_type import NumericType
from .numeric_value import NumericValue


class NumericDecoder:
    """
    Decode one numeric value from binary data.
    """


    @staticmethod
    def decode(
        data: bytes | bytearray | memoryview,
        offset: int,
        numeric_type: NumericType,
        endianness: str = "little",
    ) -> NumericValue:
        """
        Decode a numeric value.

        Parameters
        ----------
        data:
            Binary buffer.

        offset:
            Position inside buffer.

        numeric_type:
            Numeric format definition.

        endianness:
            "little" or "big".
        """

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

        buffer = bytes(data)

        end = offset + numeric_type.size

        if end > len(buffer):
            raise ValueError(
                "not enough data"
            )

        prefix = (
            "<"
            if endianness == "little"
            else ">"
        )

        value = struct.unpack_from(
            prefix + numeric_type.struct_format,
            buffer,
            offset,
        )[0]

        return NumericValue(
            offset=offset,
            numeric_type=numeric_type,
            endianness=endianness,
            value=value,
        )


    @staticmethod
    def can_decode(
        data: bytes | bytearray | memoryview,
        offset: int,
        numeric_type: NumericType,
    ) -> bool:
        """
        Check if decoding is possible.
        """

        if offset < 0:
            return False

        return (
            offset + numeric_type.size
            <= len(data)
        )


    @staticmethod
    def size_required(
        numeric_type: NumericType,
    ) -> int:
        """
        Return required byte count.
        """

        return numeric_type.size