"""
capture_recovery.parser.entropy

Statistical analysis of binary buffers.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log2


@dataclass(slots=True)
class EntropyResult:
    """
    Statistical information about a binary buffer.
    """

    size: int
    entropy: float
    histogram: tuple[int, ...]
    distinct_bytes: int
    zero_ratio: float
    printable_ratio: float


class EntropyAnalyzer:
    """
    Computes statistics on binary data.

    The implementation is allocation-friendly and uses a fixed
    histogram of 256 counters.
    """

    @staticmethod
    def analyze(data: bytes | bytearray | memoryview) -> EntropyResult:
        data = memoryview(data)

        size = len(data)

        if size == 0:
            return EntropyResult(
                size=0,
                entropy=0.0,
                histogram=(0,) * 256,
                distinct_bytes=0,
                zero_ratio=0.0,
                printable_ratio=0.0,
            )

        histogram = [0] * 256

        zero_count = 0
        printable_count = 0

        for value in data:
            histogram[value] += 1

            if value == 0:
                zero_count += 1

            if 32 <= value <= 126:
                printable_count += 1

        entropy = 0.0
        distinct = 0

        for count in histogram:
            if count:
                distinct += 1
                probability = count / size
                entropy -= probability * log2(probability)

        return EntropyResult(
            size=size,
            entropy=entropy,
            histogram=tuple(histogram),
            distinct_bytes=distinct,
            zero_ratio=zero_count / size,
            printable_ratio=printable_count / size,
        )