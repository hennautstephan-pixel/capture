from __future__ import annotations

from .segment import Segment
from .segment_detector import SegmentDetector


class BinaryInspector:
    """Facade for binary segment inspection."""

    @staticmethod
    def inspect(data: bytes) -> list[Segment]:
        return SegmentDetector.detect(data)