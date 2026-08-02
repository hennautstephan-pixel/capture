"""
capture_recovery.reverse

Public reverse analysis API.
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

from .api import (
    analyze,
    get_engine,
)

# ----------------------------------------------------------------------
# Engine
# ----------------------------------------------------------------------

from .reverse_engine import (
    ReverseEngine,
    ReverseResult,
)

from .detection_options import (
    DetectionOptions,
)

# ----------------------------------------------------------------------
# Detectors
# ----------------------------------------------------------------------

from .numeric_detector import (
    NumericDetector,
)

from .string_detector import (
    StringDetector,
)

from .guid_detector import (
    GuidDetector,
)

from .alignment_detector import (
    AlignmentDetector,
)

from .entropy_detector import (
    EntropyDetector,
)

# ----------------------------------------------------------------------
# Types
# ----------------------------------------------------------------------

from .numeric_type import *
from .string_type import *
from .guid_type import *

# ----------------------------------------------------------------------
# Values
# ----------------------------------------------------------------------

from .numeric_value import (
    NumericValue,
)

from .string_value import (
    StringValue,
)

from .guid_value import (
    GuidValue,
)

from .alignment_value import (
    AlignmentValue,
)

from .entropy_value import (
    EntropyValue,
)

__all__ = [
    # API
    "analyze",
    "get_engine",

    # Engine
    "ReverseEngine",
    "ReverseResult",
    "DetectionOptions",

    # Detectors
    "NumericDetector",
    "StringDetector",
    "GuidDetector",
    "AlignmentDetector",
    "EntropyDetector",

    # Values
    "NumericValue",
    "StringValue",
    "GuidValue",
    "AlignmentValue",
    "EntropyValue",
]