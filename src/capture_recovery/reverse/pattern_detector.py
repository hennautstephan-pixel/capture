"""
capture_recovery.reverse.pattern_detector

Generic repeated-pattern detector.

Searches repeated byte sequences inside a binary stream.

No Capture-specific knowledge is used.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Pattern:
    """
    One repeated binary pattern.
    """

    data: bytes
    length: int
    offsets: tuple[int, ...]

    @property
    def count(self) -> int:
        return len(self.offsets)


class PatternDetector:
    """
    Detect repeated byte sequences.

    Parameters
    ----------
    pattern_size
        Initial pattern size.

    min_occurrences
        Minimum number of occurrences.

    step
        Sliding window increment.

        step=1  : exhaustive scan
        step=4  : 32-bit alignment
        step=8  : 64-bit alignment
        step=16 : structure alignment
    """

    @classmethod
    def detect(
        cls,
        data: bytes | bytearray | memoryview,
        *,
        pattern_size: int = 16,
        min_occurrences: int = 2,
        step: int = 1,
    ) -> list[Pattern]:

        if pattern_size <= 0:
            raise ValueError("pattern_size must be > 0")

        if min_occurrences < 2:
            raise ValueError("min_occurrences must be >= 2")

        if step <= 0:
            raise ValueError("step must be > 0")

        if isinstance(data, memoryview):
            buffer = data.tobytes()
        else:
            buffer = bytes(data)

        index: dict[bytes, list[int]] = {}

        limit = len(buffer) - pattern_size + 1

        for offset in range(0, max(limit, 0), step):

            block = buffer[offset : offset + pattern_size]

            index.setdefault(block, []).append(offset)

        patterns: list[Pattern] = []

        for block, offsets in index.items():

            if len(offsets) < min_occurrences:
                continue

            patterns.append(
                Pattern(
                    data=block,
                    length=pattern_size,
                    offsets=tuple(offsets),
                )
            )

        patterns = cls._remove_redundant(patterns)

        patterns.sort(
            key=lambda p: (
                -p.length,
                -p.count,
                p.offsets[0],
            )
        )

        return patterns

    # -------------------------------------------------------------

    @staticmethod
    def _remove_redundant(
        patterns: list[Pattern],
    ) -> list[Pattern]:
        """
        Remove patterns that are completely contained inside a
        larger pattern with identical occurrences.
        """

        kept: list[Pattern] = []

        ordered = sorted(
            patterns,
            key=lambda p: -p.length,
        )

        for candidate in ordered:

            redundant = False

            for existing in kept:

                if (
                    candidate.offsets == existing.offsets
                    and candidate.data in existing.data
                ):
                    redundant = True
                    break

            if not redundant:
                kept.append(candidate)

        return kept

    # -------------------------------------------------------------

    @staticmethod
    def histogram(
        patterns: list[Pattern],
    ) -> dict[int, int]:
        """
        Returns a histogram of pattern lengths.

        Example
        -------
        {
            16: 42,
            24: 12,
            64: 3,
        }
        """

        hist: dict[int, int] = {}

        for pattern in patterns:
            hist[pattern.length] = (
                hist.get(pattern.length, 0) + 1
            )

        return hist

    # -------------------------------------------------------------

    @staticmethod
    def largest(
        patterns: list[Pattern],
        n: int = 10,
    ) -> list[Pattern]:
        """
        Return the n largest detected patterns.
        """

        return sorted(
            patterns,
            key=lambda p: (
                -p.length,
                -p.count,
            ),
        )[:n]

    # -------------------------------------------------------------

    @staticmethod
    def most_frequent(
        patterns: list[Pattern],
        n: int = 10,
    ) -> list[Pattern]:
        """
        Return the n most frequent patterns.
        """

        return sorted(
            patterns,
            key=lambda p: (
                -p.count,
                -p.length,
            ),
        )[:n]