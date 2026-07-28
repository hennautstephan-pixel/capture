"""
Capture binary object analyzer.

Combines binary analysis and object
candidate detection.
"""

from __future__ import annotations

from pathlib import Path


from .capture_object_detector import (
    CaptureObjectDetector,
)



class CaptureBinaryObjectAnalyzer:
    """
    Analyze possible Capture objects.
    """


    def __init__(
        self,
        detector=None,
    ):

        self.detector = (
            detector
            if detector is not None
            else CaptureObjectDetector()
        )



    def analyze(
        self,
        path,
    ) -> dict:
        """
        Analyze binary project objects.
        """


        path = Path(
            path
        )


        if not path.exists():

            raise FileNotFoundError(
                path
            )


        data = path.read_bytes()


        objects = self.detector.detect(
            data
        )


        return {

            "file": str(path),

            "size": len(data),

            "objects": objects,

            "count": len(objects),

        }