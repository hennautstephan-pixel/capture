from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from capture_recovery.io import (
    CaptureBinaryReader,
    CaptureFormatDetector,
)
from capture_recovery.parser import (
    StreamDecompressor,
)


@dataclass(slots=True, frozen=True)
class CorpusEntry:
    """
    Metadata describing one Capture sample.
    """

    path: Path

    format: str

    size: int

    sha256: str

    compressed_size: int | None

    decompressed_size: int | None

    stream_offset: int | None


@dataclass(slots=True, frozen=True)
class Corpus:
    """
    Collection of Capture samples.
    """

    entries: tuple[CorpusEntry, ...]

    @property
    def count(self) -> int:
        return len(self.entries)


class CorpusBuilder:
    """
    Build a corpus from a directory containing
    Capture sample files.
    """

    def __init__(self) -> None:

        self._reader = CaptureBinaryReader()

        self._detector = CaptureFormatDetector()

        self._decompressor = StreamDecompressor()

    def build(
        self,
        directory: str | Path,
    ) -> Corpus:

        directory = Path(directory)

        entries: list[CorpusEntry] = []

        for path in sorted(directory.rglob("*")):

            if not path.is_file():
                continue

            data = self._reader.read(path)

            file_format = self._detector.detect(path)

            compressed_size = None
            decompressed_size = None
            stream_offset = None

            if file_format == "capture_binary":

                stream_offset = (
                    self._decompressor.DEFAULT_STREAM_OFFSET
                )

                if self._decompressor.can_decompress(data):

                    stream = self._decompressor.decompress(data)

                    compressed_size = (
                        stream.compressed_size
                    )

                    decompressed_size = (
                        stream.decompressed_size
                    )

            entries.append(
                CorpusEntry(
                    path=path,
                    format=file_format,
                    size=len(data),
                    sha256=sha256(data).hexdigest(),
                    compressed_size=compressed_size,
                    decompressed_size=decompressed_size,
                    stream_offset=stream_offset,
                )
            )

        return Corpus(
            entries=tuple(entries),
        )