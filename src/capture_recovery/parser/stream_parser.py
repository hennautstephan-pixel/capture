from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StreamSection:
    """
    One logical section extracted from the stream.
    """

    offset: int

    size: int

    data: bytes


@dataclass(slots=True, frozen=True)
class CaptureStream:
    """
    Parsed Capture stream.
    """

    raw: bytes

    sections: tuple[StreamSection, ...]

    @property
    def size(self) -> int:
        return len(self.raw)

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def is_empty(self) -> bool:
        return self.size == 0


class StreamParser:
    """
    Parse a decompressed Capture stream.

    This first implementation preserves the
    complete stream as a single section.
    Later versions will split the stream into
    real Capture structures.
    """

    def parse(
        self,
        data: bytes,
    ) -> CaptureStream:

        if not data:

            return CaptureStream(
                raw=b"",
                sections=(),
            )

        section = StreamSection(
            offset=0,
            size=len(data),
            data=data,
        )

        return CaptureStream(
            raw=data,
            sections=(section,),
        )