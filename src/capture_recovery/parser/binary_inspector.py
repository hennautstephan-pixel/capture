from __future__ import annotations

from .segment import Segment
from .segment_detector import SegmentDetector


class BinaryInspector:
    """
    Runs all available binary detectors and returns discovered segments.
    """

    @classmethod
    def inspect(cls, data: bytes | bytearray | memoryview) -> list[Segment]:
        segments: list[Segment] = []

        segments.extend(SegmentDetector.detect(data))

        segments.sort(
            key=lambda s: (s.offset, s.length, s.kind)
        )

        return segments