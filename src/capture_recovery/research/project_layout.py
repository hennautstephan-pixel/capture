from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .object_mapper import (
    CandidateObject,
    ObjectMap,
)


class RegionKind(Enum):
    """
    Physical region types inside a Capture project.
    """

    HEADER = auto()
    STREAM = auto()
    FOOTER = auto()
    GAP = auto()


@dataclass(slots=True, frozen=True)
class LayoutRegion:
    """
    One physical region inside the project.
    """

    offset: int

    length: int

    kind: RegionKind

    confidence: float

    @property
    def end(self) -> int:
        return self.offset + self.length


@dataclass(slots=True, frozen=True)
class ProjectLayout:
    """
    Physical layout of a Capture project.
    """

    header: LayoutRegion

    stream: LayoutRegion

    footer: LayoutRegion

    objects: list[CandidateObject]

    gaps: list[LayoutRegion]

    @property
    def object_count(self) -> int:
        return len(self.objects)

    @property
    def gap_count(self) -> int:
        return len(self.gaps)


class ProjectLayoutBuilder:
    """
    Build a physical project layout from detected objects.

    This class does not infer Capture semantics.
    """

    def build(
        self,
        *,
        file_size: int,
        header_size: int,
        stream_offset: int,
        stream_length: int,
        footer_size: int,
        objects: ObjectMap,
    ) -> ProjectLayout:

        if file_size < 0:
            raise ValueError("file_size must be >= 0")

        if header_size < 0:
            raise ValueError("header_size must be >= 0")

        if footer_size < 0:
            raise ValueError("footer_size must be >= 0")

        if stream_offset < 0:
            raise ValueError("stream_offset must be >= 0")

        if stream_length < 0:
            raise ValueError("stream_length must be >= 0")

        if stream_offset + stream_length > file_size:
            raise ValueError(
                "stream exceeds file size"
            )

        if header_size > stream_offset:
            raise ValueError(
                "header overlaps stream"
            )

        if (
            file_size - footer_size
            < stream_offset + stream_length
        ):
            raise ValueError(
                "footer overlaps stream"
            )

        header = LayoutRegion(
            offset=0,
            length=header_size,
            kind=RegionKind.HEADER,
            confidence=1.0,
        )

        stream = LayoutRegion(
            offset=stream_offset,
            length=stream_length,
            kind=RegionKind.STREAM,
            confidence=1.0,
        )

        footer = LayoutRegion(
            offset=file_size - footer_size,
            length=footer_size,
            kind=RegionKind.FOOTER,
            confidence=1.0,
        )

        gaps = self._compute_gaps(
            stream,
            objects,
        )

        return ProjectLayout(
            header=header,
            stream=stream,
            footer=footer,
            objects=objects.by_offset(),
            gaps=gaps,
        )

    @staticmethod
    def _compute_gaps(
        stream: LayoutRegion,
        objects: ObjectMap,
    ) -> list[LayoutRegion]:

        ordered = objects.by_offset()

        if not ordered:
            return [
                LayoutRegion(
                    offset=stream.offset,
                    length=stream.length,
                    kind=RegionKind.GAP,
                    confidence=0.0,
                )
            ]

        gaps: list[LayoutRegion] = []

        current = stream.offset

        for obj in ordered:

            if obj.offset > current:

                gaps.append(
                    LayoutRegion(
                        offset=current,
                        length=obj.offset - current,
                        kind=RegionKind.GAP,
                        confidence=0.0,
                    )
                )

            current = max(
                current,
                obj.end,
            )

        if current < stream.end:

            gaps.append(
                LayoutRegion(
                    offset=current,
                    length=stream.end - current,
                    kind=RegionKind.GAP,
                    confidence=0.0,
                )
            )

        return gaps