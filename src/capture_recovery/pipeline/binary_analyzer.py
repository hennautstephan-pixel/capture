"""
Binary analyzer.

Connects binary data with the
existing detector system.
"""

from __future__ import annotations


class BinaryAnalyzer:
    """
    Analyze raw binary Capture data.
    """

    def __init__(
        self,
        detectors=None,
    ) -> None:

        self.detectors = (
            detectors
            or []
        )


    def analyze(
        self,
        data: bytes,
    ) -> list:
        """
        Run all detectors.

        Returns detected elements.
        """

        detections = []


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
    ) -> dict:
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