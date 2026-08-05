"""
Binary analyzer.

Connects binary data with the
existing detector system.
"""

from __future__ import annotations

from capture_recovery.models.detection import Detection

from capture_recovery.detectors import (
    AsciiDetector,
    FloatDetector,
    IntegerDetector,
    SignatureDetector,
)

from .types import BinarySummaryDict


class BinaryAnalyzer:
    """
    Analyze raw binary Capture data.

    Uses default binary detectors when no
    detector list is provided.
    """


    def __init__(
        self,
        detectors: list | None = None,
    ) -> None:

        self.detectors: list = (
            detectors
            if detectors is not None
            else self._default_detectors()
        )


    @staticmethod
    def _default_detectors() -> list:
        """
        Build default detectors.

        The order is intentional:
        signatures and text have higher semantic
        value than generic numeric detections.
        """

        return [
            SignatureDetector(),

            AsciiDetector(),

            IntegerDetector(),

            FloatDetector(),
        ]


    def analyze(
        self,
        data: bytes,
    ) -> list[Detection]:
        """
        Run all detectors.

        Returns detected elements.
        """

        detections: list[Detection] = []


        for detector in self.detectors:

            results = detector.detect(
                data,
            )

            detections.extend(
                results,
            )


        detections.sort(
            key=lambda item: (
                item.offset,
                item.length,
            )
        )


        return detections


    def summary(
        self,
        data: bytes,
    ) -> BinarySummaryDict:
        """
        Return binary analysis summary.

        Keeps compatibility with
        existing pipeline tests.
        """

        detections = self.analyze(
            data,
        )


        return {
            "size": len(data),

            "count": len(
                detections,
            ),

            "detections": detections,

            # compatibility API
            "index": detections,
        }

