"""
capture_recovery.reverse.entropy_detector

Detect high entropy binary regions.
"""

from __future__ import annotations

import math
from collections import Counter

from .base_detector import BaseDetector
from .detection_options import DetectionOptions
from .detector_type import DetectorType
from .entropy_value import EntropyValue


class EntropyDetector(BaseDetector):
    """
    Detect entropy levels in binary buffers.
    """

    detector_type = DetectorType.ENTROPY

    def __init__(
        self,
        block_size: int = 256,
    ) -> None:

        if block_size <= 0:
            raise ValueError(
                "block_size must be > 0"
            )

        self._block_size = block_size

    @property
    def name(self) -> str:
        """
        Detector public name.
        """
        return "entropy"

    def detect(
        self,
        data: bytes | bytearray | memoryview,
        options: DetectionOptions | None = None,
        minimum_entropy: float = 6.0,
    ) -> list[EntropyValue]:
        """
        Detect high entropy blocks.
        """

        if options is None:
            options = DetectionOptions()

        if not self._is_enabled(
            options,
            self.detector_type,
        ):
            return []

        buffer = self._buffer(
            data,
            options,
        )

        results: list[EntropyValue] = []

        for offset in range(
            0,
            len(buffer),
            self._block_size,
        ):

            block = bytes(
                buffer[
                    offset:
                    offset + self._block_size
                ]
            )

            if not block:
                continue

            entropy = self.calculate_entropy(
                block
            )

            if entropy < minimum_entropy:
                continue

            results.append(
                EntropyValue(
                    offset=offset,
                    entropy=entropy,
                    length=len(block),
                    score=entropy / 8,
                )
            )

        return list(
            self._limit_results(
                results,
                options,
            )
        )

    @staticmethod
    def calculate_entropy(
        data: bytes,
    ) -> float:
        """
        Calculate Shannon entropy.
        """

        if not data:
            return 0.0

        length = len(data)

        counts = Counter(
            data
        )

        entropy = 0.0

        for count in counts.values():

            probability = (
                count / length
            )

            entropy -= (
                probability
                * math.log2(
                    probability
                )
            )

        return entropy

    @property
    def block_size(
        self,
    ) -> int:
        """
        Current block size.
        """
        return self._block_size