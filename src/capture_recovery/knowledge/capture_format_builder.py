from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from capture_recovery.parser.ascii_detector import AsciiDetector

from .capture_format import (
    CaptureField,
    CaptureFormat,
)

from collections.abc import Iterable

class CaptureFormatBuilder:
    """
    Build a CaptureFormat from a corpus of .c2p files.

    Version 1:
      - scans ASCII strings using the existing AsciiDetector
      - computes occurrence frequency
      - computes the most common offset
      - estimates confidence from the corpus

    Future versions will enrich the format with GUIDs,
    integers, float matrices, object signatures...
    """

    def build(
        self,
        corpus: str | Path,
    ) -> CaptureFormat:

        corpus = Path(corpus)

        if not corpus.exists():
            raise FileNotFoundError(corpus)

        files = tuple(self._iter_files(corpus))

        if not files:
            return CaptureFormat()

        observations = self._collect_ascii(files)

        return self._build_ascii_format(
            observations,
            len(files),
        )

    def _iter_files(
        self,
        corpus: Path,
    ) -> Iterable[Path]:

        yield from sorted(
            corpus.rglob("*.c2p"),
        )

    def _collect_ascii(
        self,
        files: Iterable[Path],
    ) -> dict[str, list[tuple[int, int]]]:

        observations: dict[
            str,
            list[tuple[int, int]],
        ] = defaultdict(list)

        for file in files:

            data = file.read_bytes()

            for segment in AsciiDetector.detect(data):

                text = segment.metadata.get("text")

                if not text:
                    continue

                observations[text].append(
                    (
                        segment.offset,
                        segment.length,
                    )
                )

        return observations

    def _build_ascii_format(
        self,
        observations: dict[str, list[tuple[int, int]]],
        file_count: int,
    ) -> CaptureFormat:

        fmt = CaptureFormat()

        for text, values in sorted(observations.items()):

            offsets = [
                offset
                for offset, _ in values
            ]

            lengths = [
                length
                for _, length in values
            ]

            offset = max(
                set(offsets),
                key=offsets.count,
            )

            size = max(lengths)

            confidence = (
                len(values)
                / file_count
            )

            fmt.add_field(
                CaptureField(
                    name=text,
                    offset=offset,
                    size=size,
                    confidence=confidence,
                    metadata={
                        "encoding": "ascii",
                        "occurrences": len(values),
                        "files": file_count,
                        "status": (
                            "confirmed"
                            if confidence == 1.0
                            else "observed"
                        ),
                    },
                )
            )

        return fmt

    