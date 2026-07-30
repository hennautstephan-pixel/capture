"""
Binary analyzer.

Connects binary data with the
existing detector system.
"""

from __future__ import annotations

from capture_recovery.models.detection import Detection
from .types import BinarySummaryDict


class BinaryAnalyzer:
    """
    Analyze raw binary Capture data.
    """

    def __init__(
        self,
        detectors: list | None = None,
    ) -> None:

        self.detectors: list = (
            detectors
            or []
        )


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
                results
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
                detections
            ),

            "detections": detections,

            # compatibility API
            "index": detections,

        }