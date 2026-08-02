from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CaptureHeader:
    """
    Parsed Capture project header.

    Unknown fields are intentionally preserved
    to support future reverse engineering.
    """

    raw: bytes

    magic: bytes

    version: int | None

    header_size: int

    payload_offset: int | None

    flags: int | None

    @property
    def is_valid(self) -> bool:
        return bool(self.magic)

    @property
    def size(self) -> int:
        return len(self.raw)


class HeaderParser:
    """
    Parse the header of a Capture project.

    At this stage only a small subset of the
    format is decoded. Unknown bytes remain
    available through ``raw``.
    """

    DEFAULT_HEADER_SIZE = 32

    def parse(
        self,
        data: bytes,
    ) -> CaptureHeader:

        if not data:
            return CaptureHeader(
                raw=b"",
                magic=b"",
                version=None,
                header_size=0,
                payload_offset=None,
                flags=None,
            )

        header = data[: self.DEFAULT_HEADER_SIZE]

        magic = header[:8]

        version = (
            int.from_bytes(
                header[8:12],
                "little",
            )
            if len(header) >= 12
            else None
        )

        payload_offset = (
            int.from_bytes(
                header[12:16],
                "little",
            )
            if len(header) >= 16
            else None
        )

        flags = (
            int.from_bytes(
                header[16:20],
                "little",
            )
            if len(header) >= 20
            else None
        )

        return CaptureHeader(
            raw=header,
            magic=magic,
            version=version,
            header_size=len(header),
            payload_offset=payload_offset,
            flags=flags,
        )