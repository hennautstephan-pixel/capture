"""
Common infrastructure for reverse detectors.

This module intentionally contains only shared helper methods.
No detector depends on this class yet (Commit 1A).
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import Any

from .detection_options import DetectionOptions
from .detector_type import DetectorType


class BaseDetector(ABC):
    """Base class for reverse detectors.

    Commit 1A only introduces shared utilities.
    Existing detectors keep their current implementation unchanged.
    """

    detector_type: DetectorType

    @staticmethod
    def _is_enabled(
        options: DetectionOptions,
        detector_type: DetectorType,
    ) -> bool:
        """Return True if this detector is enabled."""
        enabled = options.enabled_types
        return enabled is None or detector_type in enabled

    @staticmethod
    def _buffer(
        data: bytes | bytearray | memoryview,
        options: DetectionOptions,
    ) -> memoryview:
        """Return a bounded memory view of the input buffer."""
        view = memoryview(data)

        if options.max_scan_size is not None:
            view = view[: options.max_scan_size]

        return view

    @staticmethod
    def _limit_results[T](
        results: Sequence[T],
        options: DetectionOptions,
    ) -> tuple[T, ...]:
        """Apply the global max_results option if defined."""
        if options.max_results is None:
            return tuple(results)

        return tuple(results[: options.max_results])

    @staticmethod
    def _offset_in_range(
        offset: int,
        buffer_size: int,
    ) -> bool:
        """Small helper for bounds checking."""
        return 0 <= offset < buffer_size

    @property
    def name(self) -> str:
        """Default detector name."""
        return self.__class__.__name__