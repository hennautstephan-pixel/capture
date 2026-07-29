from __future__ import annotations

from ..models.detection import Detection
from .segment import Segment


class DetectionAdapter:
    """
    Convert existing Detection objects into parser Segment objects.
    """

    @staticmethod
    def to_segment(detection: Detection) -> Segment:
        metadata = {}

        if getattr(detection, "value", None) is not None:
            metadata["value"] = detection.value

        return Segment(
            offset=detection.offset,
            length=detection.length,
            kind=detection.datatype,
            confidence=detection.confidence,
            metadata=metadata,
        )

    @staticmethod
    def to_segments(
        detections: list[Detection],
    ) -> list[Segment]:
        return [
            DetectionAdapter.to_segment(d)
            for d in detections
        ]