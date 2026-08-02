from __future__ import annotations

from .stream import CaptureStream
from .stream_locator import CaptureStreamLocator
from .stream_scanner import CaptureStreamScanner


class CaptureStreamParser:
    """
    Build CaptureStream objects from candidate stream regions.
    """

    def __init__(
        self,
        scanner: CaptureStreamScanner | None = None,
        locator: CaptureStreamLocator | None = None,
    ) -> None:

        self._scanner = scanner or CaptureStreamScanner()
        self._locator = locator or CaptureStreamLocator(
            scanner=self._scanner,
        )

    @property
    def scanner(self) -> CaptureStreamScanner:
        return self._scanner

    @property
    def locator(self) -> CaptureStreamLocator:
        return self._locator

    def parse(
        self,
        data: bytes,
    ) -> list[CaptureStream]:

        streams: list[CaptureStream] = []

        for region in self._locator.locate(data):

            signature = region.signature

            if signature == b"\x78\x01":
                compression = "zlib-0"

            elif signature == b"\x78\x5E":
                compression = "zlib-1"

            elif signature == b"\x78\x9C":
                compression = "zlib"

            elif signature == b"\x78\xDA":
                compression = "zlib-9"

            else:
                compression = "unknown"

            streams.append(
                CaptureStream(
                    offset=region.start,
                    compressed_size=len(region),
                    raw=data[
                        region.start:region.end
                    ],
                    compression=compression,
                )
            )

        return streams

    def first(
        self,
        data: bytes,
    ) -> CaptureStream | None:

        streams = self.parse(data)

        if streams:
            return streams[0]

        return None