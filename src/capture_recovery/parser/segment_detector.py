"""
capture_recovery.parser.segment_detector

Automatic detection of interesting regions in a binary buffer.
"""

from __future__ import annotations

import zlib

from .entropy import EntropyAnalyzer
from .segment import Segment


class SegmentDetector:
    """
    Detects simple binary regions.

    Current version detects:
        - all-zero buffers
        - printable ASCII buffers
        - probable zlib streams
        - high-entropy binary regions
    """

    ZLIB_HEADERS = (
        b"\x78\x01",
        b"\x78\x5E",
        b"\x78\x9C",
        b"\x78\xDA",
    )

    @classmethod
    def detect(cls, data: bytes | bytearray | memoryview) -> list[Segment]:
        data = memoryview(data)

        if len(data) == 0:
            return []

        raw = data.tobytes()

        result: list[Segment] = []

        stats = EntropyAnalyzer.analyze(data)

        # ------------------------------------------------------------------
        # Zero-filled region
        # ------------------------------------------------------------------

        if stats.zero_ratio == 1.0:
            result.append(
                Segment(
                    offset=0,
                    length=len(data),
                    kind="zero",
                    confidence=1.0,
                )
            )
            return result

        # ------------------------------------------------------------------
        # Printable ASCII
        # ------------------------------------------------------------------

        if stats.printable_ratio >= 0.95:
            result.append(
                Segment(
                    offset=0,
                    length=len(data),
                    kind="ascii",
                    confidence=stats.printable_ratio,
                )
            )

        # ------------------------------------------------------------------
        # zlib
        # ------------------------------------------------------------------

        if raw.startswith(cls.ZLIB_HEADERS):
            try:
                zlib.decompress(raw)

                result.append(
                    Segment(
                        offset=0,
                        length=len(data),
                        kind="zlib",
                        confidence=1.0,
                    )
                )

            except zlib.error:
                pass

        # ------------------------------------------------------------------
        # High entropy
        # ------------------------------------------------------------------

        if stats.entropy >= 7.5:
            result.append(
                Segment(
                    offset=0,
                    length=len(data),
                    kind="binary",
                    confidence=min(stats.entropy / 8.0, 1.0),
                    metadata={
                        "entropy": stats.entropy,
                    },
                )
            )

        if not result:
            result.append(
                Segment(
                    offset=0,
                    length=len(data),
                    kind="unknown",
                    confidence=0.0,
                )
            )

        return result