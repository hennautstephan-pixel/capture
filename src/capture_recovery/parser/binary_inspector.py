from __future__ import annotations

from .segment import Segment
from .segment_detector import SegmentDetector


class BinaryInspector:

    @classmethod
    def inspect(cls, data: bytes) -> list[Segment]:

        return SegmentDetector.detect(data)