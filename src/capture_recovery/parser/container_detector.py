from __future__ import annotations

from dataclasses import dataclass

from .segment import Segment
from .segment_detector import SegmentDetector


@dataclass(slots=True)
class Container:
    offset: int
    length: int
    kind: str
    confidence: float = 1.0
    metadata: dict[str, object] | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length


class ContainerDetector:
    """
    Build logical containers from parser segments.

    This is the first abstraction layer above SegmentDetector.
    """

    _MAPPING = {
        "zip": "zip",
        "gzip": "gzip",
        "xml": "xml",
        "zlib": "zlib",
        "pdf": "pdf",
        "png": "png",
        "jpeg": "jpeg",
        "gif87a": "gif",
        "gif89a": "gif",
        "sqlite": "sqlite",
        "riff": "riff",
    }

    @classmethod
    def detect(
        cls,
        data: bytes | bytearray | memoryview,
    ) -> list[Container]:

        containers: list[Container] = []

        for segment in SegmentDetector.detect(data):

            kind = cls._MAPPING.get(segment.kind)

            if kind is None:
                continue

            containers.append(
                Container(
                    offset=segment.offset,
                    length=segment.length,
                    kind=kind,
                    confidence=segment.confidence,
                    metadata=dict(segment.metadata),
                )
            )

        return containers