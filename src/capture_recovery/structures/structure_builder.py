from __future__ import annotations

from capture_recovery.indexes import DetectionIndex
from capture_recovery.models import Detection

from .field import Field
from .structure import Structure


class StructureBuilder:
    """
    Build high-level structures from a DetectionIndex.

    The initial implementation groups detections that are contiguous
    or separated by only a few bytes.
    """

    def __init__(self, max_gap: int = 8) -> None:

        self.max_gap = max_gap

    def build(self, index: DetectionIndex) -> list[Structure]:

        detections = sorted(index.all(), key=lambda d: d.offset)

        if not detections:
            return []

        structures: list[Structure] = []

        current: list[Detection] = [detections[0]]

        for detection in detections[1:]:

            previous = current[-1]

            gap = detection.offset - previous.end

            if gap <= self.max_gap:
                current.append(detection)
            else:
                structures.append(self._build_structure(current))
                current = [detection]

        structures.append(self._build_structure(current))

        return structures

    def _build_structure(
        self,
        detections: list[Detection],
    ) -> Structure:

        first = detections[0]
        last = detections[-1]

        structure = Structure(
            name="Structure",
            offset=first.offset,
            length=last.end - first.offset,
        )

        for i, detection in enumerate(detections):

            structure.add(
                Field(
                    name=f"field_{i}",
                    offset=detection.offset,
                    length=detection.length,
                    datatype=detection.datatype,
                    value=detection.value,
                    confidence=detection.confidence,
                )
            )

        return structure