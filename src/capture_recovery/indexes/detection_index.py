from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections import defaultdict

from ..models import Detection


class DetectionIndex:
    """Index optimisé pour rechercher rapidement des détections."""

    def __init__(self, detections: list[Detection]) -> None:

        self._detections = sorted(
            detections,
            key=lambda d: d.offset,
        )

        self._offsets = [d.offset for d in self._detections]

        self._by_type: dict[str, list[Detection]] = defaultdict(list)

        for detection in self._detections:
            self._by_type[detection.datatype].append(detection)

    def __len__(self) -> int:
        return len(self._detections)

    def __iter__(self):
        return iter(self._detections)

    def all(self) -> list[Detection]:
        return list(self._detections)

    def by_type(self, datatype: str) -> list[Detection]:
        return list(self._by_type.get(datatype, []))

    def at(self, offset: int) -> list[Detection]:
        """Retourne les détections qui commencent exactement à offset."""

        left = bisect_left(self._offsets, offset)
        right = bisect_right(self._offsets, offset)

        return self._detections[left:right]

    def before(self, offset: int) -> list[Detection]:
        """Toutes les détections avant un offset."""

        index = bisect_left(self._offsets, offset)

        return self._detections[:index]

    def after(self, offset: int) -> list[Detection]:
        """Toutes les détections à partir d'un offset."""

        index = bisect_right(self._offsets, offset)

        return self._detections[index:]

    def range(self, start: int, end: int) -> list[Detection]:
        """Toutes les détections dont l'offset est compris dans [start, end)."""

        left = bisect_left(self._offsets, start)
        right = bisect_left(self._offsets, end)

        return self._detections[left:right]

    def overlapping(self, start: int, end: int) -> list[Detection]:
        """Détections qui chevauchent un intervalle."""

        return [
            d
            for d in self._detections
            if d.offset < end and d.end > start
        ]