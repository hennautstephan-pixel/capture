from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class CaptureStream:
    """
    Compressed stream found inside a Capture (.c2p) file.
    """

    offset: int

    compressed_size: int

    raw: bytes = field(default_factory=bytes)

    compression: str = "zlib"

    @property
    def end_offset(self) -> int:
        return self.offset + self.compressed_size

    @property
    def is_empty(self) -> bool:
        return self.compressed_size == 0

    def contains(
        self,
        offset: int,
    ) -> bool:
        return self.offset <= offset < self.end_offset

    def __len__(self) -> int:
        return self.compressed_size