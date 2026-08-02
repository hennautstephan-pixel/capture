from __future__ import annotations

from pathlib import Path

from capture_recovery.io import CaptureBinaryReader
from capture_recovery.parser import StreamDecompressor


class StreamSampleLoader:
    """
    Load and decompress Capture sample files.
    """

    def __init__(self) -> None:

        self._reader = CaptureBinaryReader()

        self._decompressor = StreamDecompressor()

    def load(
        self,
        path: str | Path,
    ) -> bytes:

        path = Path(path)

        content = self._reader.read(
            path,
        )

        result = self._decompressor.decompress(
            content,
        )

        return result.decompressed