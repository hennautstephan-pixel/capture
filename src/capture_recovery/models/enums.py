"""
Shared enumerations used by the Capture Recovery project.
"""

from enum import Enum


class Severity(Enum):
    """Importance level of a finding."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class FindingType(Enum):
    """Supported finding categories."""

    ASCII = "ascii"
    UTF16 = "utf16"

    INTEGER = "integer"
    FLOAT = "float"
    DOUBLE = "double"

    POINTER = "pointer"

    SIGNATURE = "signature"
    PATTERN = "pattern"

    HEADER = "header"

    BLOCK = "block"

    UNKNOWN = "unknown"


class BlockType(Enum):
    """High level block classification."""

    UNKNOWN = "unknown"

    HEADER = "header"

    METADATA = "metadata"

    DATA = "data"

    COMPRESSED = "compressed"

    PADDING = "padding"