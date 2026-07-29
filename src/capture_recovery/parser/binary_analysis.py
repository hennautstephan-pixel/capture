"""
capture_recovery.parser.binary_analysis

Container for the complete analysis of a binary file.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .segment import Segment


@dataclass(slots=True)
class BinaryAnalysis:
    """
    Complete binary analysis.

    This object aggregates every piece of information discovered
    while analysing a Capture binary file.
    """

    size: int = 0

    segments: list[Segment] = field(default_factory=list)

    detections: list[object] = field(default_factory=list)

    strings: list[str] = field(default_factory=list)

    signatures: list[object] = field(default_factory=list)

    inferred_objects: list[object] = field(default_factory=list)

    relations: list[object] = field(default_factory=list)

    statistics: dict[str, object] = field(default_factory=dict)

    metadata: dict[str, object] = field(default_factory=dict)

    @property
    def segment_count(self) -> int:
        return len(self.segments)

    @property
    def detection_count(self) -> int:
        return len(self.detections)

    def add_segment(self, segment: Segment) -> None:
        self.segments.append(segment)

    def add_detection(self, detection: object) -> None:
        self.detections.append(detection)

    def add_string(self, value: str) -> None:
        self.strings.append(value)

    def add_signature(self, signature: object) -> None:
        self.signatures.append(signature)

    def add_object(self, obj: object) -> None:
        self.inferred_objects.append(obj)

    def add_relation(self, relation: object) -> None:
        self.relations.append(relation)