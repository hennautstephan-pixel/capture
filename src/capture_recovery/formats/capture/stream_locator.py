from __future__ import annotations

import zlib

from .stream_region import CaptureStreamRegion
from .stream_scanner import CaptureStreamScanner


class CaptureStreamLocator:
    """
    Locate candidate compressed stream regions.

    Strategy:

    1. Try to determine the exact stream length using zlib.
    2. If that fails, fall back to the next detected signature.
    """

    def __init__(
        self,
        scanner: CaptureStreamScanner | None = None,
    ) -> None:

        self._scanner = scanner or CaptureStreamScanner()

    @property
    def scanner(self) -> CaptureStreamScanner:
        return self._scanner

    def locate(
        self,
        data: bytes,
    ) -> list[CaptureStreamRegion]:

        offsets = self._scanner.find(data)

        if not offsets:
            return []

        regions: list[CaptureStreamRegion] = []

        for index, start in enumerate(offsets):

            next_offset = (
                offsets[index + 1]
                if index + 1 < len(offsets)
                else len(data)
            )

            regions.append(
                self._locate_stream(
                    data=data,
                    start=start,
                    fallback_end=next_offset,
                )
            )

        return regions

    def first(
        self,
        data: bytes,
    ) -> CaptureStreamRegion | None:

        regions = self.locate(data)

        if regions:
            return regions[0]

        return None

    def _locate_stream(
        self,
        data: bytes,
        start: int,
        fallback_end: int,
    ) -> CaptureStreamRegion:

        raw = data[start:]

        consumed: int | None = None
        end = fallback_end

        try:

            decompressor = zlib.decompressobj()

            decompressor.decompress(raw)

            consumed = len(raw) - len(
                decompressor.unused_data
            )

            if consumed > 0:
                end = start + consumed

        except zlib.error:
            # Invalid or incomplete stream:
            # keep the fallback region.
            pass

        return CaptureStreamRegion(
            start=start,
            end=end,
            signature=data[start:start + 2],
            bytes_consumed=consumed,
        )