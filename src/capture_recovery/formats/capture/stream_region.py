from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CaptureStreamRegion:
    """
    Region occupied by one compressed stream.
    """

    start: int

    end: int

    signature: bytes

    bytes_consumed: int | None = None

    @property
    def size(self) -> int:
        return self.end - self.start

    @property
    def is_empty(self) -> bool:
        return self.size <= 0

    def contains(
        self,
        offset: int,
    ) -> bool:
        return self.start <= offset < self.end

    def __len__(self) -> int:
        return self.size