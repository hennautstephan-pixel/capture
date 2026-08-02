from __future__ import annotations

import zlib
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DecompressedStream:
    """
    Result of a Capture stream decompression.
    """

    compressed: bytes

    decompressed: bytes

    offset: int

    @property
    def compressed_size(self) -> int:
        return len(self.compressed)

    @property
    def decompressed_size(self) -> int:
        return len(self.decompressed)

    @property
    def compression_ratio(self) -> float:
        if not self.compressed:
            return 0.0

        return (
            self.decompressed_size
            / self.compressed_size
        )

    @property
    def is_empty(self) -> bool:
        return self.decompressed_size == 0


class StreamDecompressor:
    """
    Decompress the binary payload of a Capture project.

    The default stream offset is currently based on
    reverse engineering observations and will later
    be provided by HeaderParser.
    """

    DEFAULT_STREAM_OFFSET = 62

    def decompress(
        self,
        data: bytes,
        *,
        offset: int | None = None,
    ) -> DecompressedStream:

        if offset is None:
            offset = self.DEFAULT_STREAM_OFFSET

        if offset < 0:
            raise ValueError(
                "Offset must be positive."
            )

        if offset > len(data):
            raise ValueError(
                "Offset exceeds file size."
            )

        compressed = data[offset:]

        if not compressed:

            return DecompressedStream(
                compressed=b"",
                decompressed=b"",
                offset=offset,
            )

        decompressed = zlib.decompress(
            compressed,
        )

        return DecompressedStream(
            compressed=compressed,
            decompressed=decompressed,
            offset=offset,
        )

    def can_decompress(
        self,
        data: bytes,
        *,
        offset: int | None = None,
    ) -> bool:

        try:

            self.decompress(
                data,
                offset=offset,
            )

            return True

        except (
            ValueError,
            zlib.error,
        ):

            return False