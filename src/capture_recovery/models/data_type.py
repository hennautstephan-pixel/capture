from __future__ import annotations

from enum import StrEnum, auto


class DataType(StrEnum):
    """
    Logical data types detected inside a Capture project.

    These values describe the semantic interpretation of binary data,
    independently of the detector that produced them.
    """

    # ------------------------------------------------------------------
    # Unknown / raw data
    # ------------------------------------------------------------------

    UNKNOWN = auto()
    BYTES = auto()
    SIGNATURE = auto()

    # ------------------------------------------------------------------
    # Boolean
    # ------------------------------------------------------------------

    BOOLEAN = auto()

    # ------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------

    STRING = auto()

    ASCII = auto()
    UTF8 = auto()
    UTF16 = auto()

    # ------------------------------------------------------------------
    # Integer values
    # ------------------------------------------------------------------

    INT8 = auto()
    UINT8 = auto()

    INT16 = auto()
    UINT16 = auto()

    INT32 = auto()
    UINT32 = auto()

    INT64 = auto()
    UINT64 = auto()

    # ------------------------------------------------------------------
    # Floating-point values
    # ------------------------------------------------------------------

    FLOAT32 = auto()
    FLOAT64 = auto()

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    VECTOR2 = auto()
    VECTOR3 = auto()
    VECTOR4 = auto()

    MATRIX3 = auto()
    MATRIX4 = auto()

    QUATERNION = auto()

    # ------------------------------------------------------------------
    # Colors
    # ------------------------------------------------------------------

    COLOR_RGB = auto()
    COLOR_RGBA = auto()

    # ------------------------------------------------------------------
    # Identifiers
    # ------------------------------------------------------------------

    UUID = auto()

    # ------------------------------------------------------------------
    # Arrays
    # ------------------------------------------------------------------

    ARRAY = auto()

    BYTE_ARRAY = auto()
    INTEGER_ARRAY = auto()
    FLOAT_ARRAY = auto()
    STRING_ARRAY = auto()

    # ------------------------------------------------------------------
    # Reverse engineering
    # ------------------------------------------------------------------

    POINTER = auto()
    OFFSET = auto()

    STRUCT = auto()
    TABLE = auto()

    CURVE = auto()

    OBJECT = auto()
    UNKNOWN_OBJECT = auto()

    # ------------------------------------------------------------------
    # Time
    # ------------------------------------------------------------------

    TIMESTAMP = auto()
    DATETIME = auto()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def is_text(self) -> bool:
        """Return True if this is a text datatype."""
        return self in {
            DataType.STRING,
            DataType.ASCII,
            DataType.UTF8,
            DataType.UTF16,
        }

    @property
    def is_integer(self) -> bool:
        """Return True if this is an integer datatype."""
        return self in {
            DataType.INT8,
            DataType.UINT8,
            DataType.INT16,
            DataType.UINT16,
            DataType.INT32,
            DataType.UINT32,
            DataType.INT64,
            DataType.UINT64,
        }

    @property
    def is_float(self) -> bool:
        """Return True if this is a floating-point datatype."""
        return self in {
            DataType.FLOAT32,
            DataType.FLOAT64,
        }

    @property
    def is_numeric(self) -> bool:
        """Return True if this datatype represents a numeric value."""
        return self.is_integer or self.is_float

    @property
    def is_array(self) -> bool:
        """Return True if this datatype represents an array."""
        return self in {
            DataType.ARRAY,
            DataType.BYTE_ARRAY,
            DataType.INTEGER_ARRAY,
            DataType.FLOAT_ARRAY,
            DataType.STRING_ARRAY,
        }

    @property
    def is_vector(self) -> bool:
        """Return True if this datatype is a vector."""
        return self in {
            DataType.VECTOR2,
            DataType.VECTOR3,
            DataType.VECTOR4,
        }

    @property
    def is_matrix(self) -> bool:
        """Return True if this datatype is a matrix."""
        return self in {
            DataType.MATRIX3,
            DataType.MATRIX4,
        }

    @property
    def is_color(self) -> bool:
        """Return True if this datatype represents a color."""
        return self in {
            DataType.COLOR_RGB,
            DataType.COLOR_RGBA,
        }

    @property
    def is_pointer(self) -> bool:
        """Return True if this datatype represents a pointer or offset."""
        return self in {
            DataType.POINTER,
            DataType.OFFSET,
        }

    @property
    def is_complex(self) -> bool:
        """Return True for structured or high-level objects."""
        return self in {
            DataType.STRUCT,
            DataType.TABLE,
            DataType.CURVE,
            DataType.OBJECT,
            DataType.UNKNOWN_OBJECT,
        }

    def __str__(self) -> str:
        return self.value