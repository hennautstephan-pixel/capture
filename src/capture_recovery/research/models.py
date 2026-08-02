from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class CorpusStream:
    """
    One compressed stream found in a Capture project.
    """

    offset: int

    compressed_size: int

    decompressed_size: int

    trailing_bytes: int

    footer: bytes

    decompressed: bytes


@dataclass(slots=True, frozen=True)
class CorpusAnalysis:
    """
    Result of analysing one Capture project.
    """

    path: Path

    file_size: int

    stream: CorpusStream

    header_size: int