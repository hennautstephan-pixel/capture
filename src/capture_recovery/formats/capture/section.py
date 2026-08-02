from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CaptureSection:
    """
    Raw section extracted from a Capture (.c2p) file.

    At this stage of the reverse engineering process, a section
    is only defined by its position and raw payload.
    """

    offset: int

    size: int

    raw: bytes

    @property
    def end_offset(self) -> int:
        """
        Return the offset immediately after this section.
        """
        return self.offset + self.size

    @property
    def is_empty(self) -> bool:
        """
        Return True if the section contains no payload.
        """
        return self.size == 0

    def contains(
        self,
        offset: int,
    ) -> bool:
        """
        Return True if the given file offset belongs
        to this section.
        """
        return self.offset <= offset < self.end_offset

    def __len__(self) -> int:
        return self.size