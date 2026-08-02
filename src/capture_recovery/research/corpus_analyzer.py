from __future__ import annotations

from pathlib import Path
import zlib

from .models import (
    CorpusAnalysis,
    CorpusStream,
)


class CorpusAnalyzer:
    """
    Analyse one Capture project.

    This class performs objective measurements only.
    It never assumes knowledge of the Capture format.
    """

    HEADER_SIGNATURE = b"\x78\x9C"

    def analyze(
        self,
        path: str | Path,
    ) -> CorpusAnalysis:

        path = Path(path)

        data = path.read_bytes()

        offset = data.index(self.HEADER_SIGNATURE)

        raw = data[offset:]

        decompressor = zlib.decompressobj()

        try:
            payload = decompressor.decompress(raw)

            consumed = len(raw) - len(
                decompressor.unused_data
            )

            footer = decompressor.unused_data

        except zlib.error:
            payload = b""
            consumed = 0
            footer = b""

        stream = CorpusStream(
            offset=offset,
            compressed_size=consumed,
            decompressed_size=len(payload),
            trailing_bytes=len(footer),
            footer=footer,
            decompressed=payload,
        )

        return CorpusAnalysis(
            path=path,
            file_size=len(data),
            stream=stream,
            header_size=offset,
        )