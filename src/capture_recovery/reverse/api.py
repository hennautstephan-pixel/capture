"""
capture_recovery.reverse.api

Public API for reverse analysis.
"""

from __future__ import annotations

from .detection_options import DetectionOptions
from .reverse_engine import (
    ReverseEngine,
    ReverseResult,
)


# Singleton engine
_ENGINE = ReverseEngine()



def analyze(
    data: bytes | bytearray | memoryview,
    options: DetectionOptions | None = None,
) -> ReverseResult:
    """
    Analyze binary data.

    Parameters
    ----------
    data:
        Binary buffer.

    options:
        Detection configuration.

    Returns
    -------
    ReverseResult
    """

    return _ENGINE.analyze(
        bytes(data),
        options,
    )



def get_engine() -> ReverseEngine:
    """
    Return shared ReverseEngine instance.
    """

    return _ENGINE



__all__ = [
    "analyze",
    "get_engine",
    "ReverseResult",
]