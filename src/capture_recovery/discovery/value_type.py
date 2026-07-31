"""
Supported property value types.
"""

from __future__ import annotations

from enum import StrEnum


class ValueType(StrEnum):
    """
    Supported value types for property discovery.
    """

    BOOL = "bool"

    INT8 = "int8"
    UINT8 = "uint8"

    INT16 = "int16"
    UINT16 = "uint16"

    INT32 = "int32"
    UINT32 = "uint32"

    INT64 = "int64"
    UINT64 = "uint64"

    FLOAT32 = "float32"
    FLOAT64 = "float64"

    STRING = "string"

    BYTES = "bytes"

    UNKNOWN = "unknown"

    @property
    def is_integer(self) -> bool:
        """
        True if this represents an integer type.
        """
        return self in {
            ValueType.INT8,
            ValueType.UINT8,
            ValueType.INT16,
            ValueType.UINT16,
            ValueType.INT32,
            ValueType.UINT32,
            ValueType.INT64,
            ValueType.UINT64,
        }

    @property
    def is_float(self) -> bool:
        """
        True if this represents a floating-point type.
        """
        return self in {
            ValueType.FLOAT32,
            ValueType.FLOAT64,
        }

    @property
    def is_numeric(self) -> bool:
        """
        True if this represents any numeric type.
        """
        return self.is_integer or self.is_float

    @property
    def is_signed(self) -> bool:
        """
        True if this represents a signed integer.
        """
        return self in {
            ValueType.INT8,
            ValueType.INT16,
            ValueType.INT32,
            ValueType.INT64,
        }

    @property
    def is_unsigned(self) -> bool:
        """
        True if this represents an unsigned integer.
        """
        return self in {
            ValueType.UINT8,
            ValueType.UINT16,
            ValueType.UINT32,
            ValueType.UINT64,
        }