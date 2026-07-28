"""
Capture signature analyzer.

High level analysis of repeated
binary structures inside Capture files.
"""

from __future__ import annotations

from pathlib import Path


from .capture_signature_detector import (
    CaptureSignatureDetector,
)



class CaptureSignatureAnalyzer:
    """
    Analyze binary signatures from Capture projects.
    """



    def __init__(
        self,
        detector=None,
    ):

        self.detector = (

            detector

            if detector is not None

            else CaptureSignatureDetector(
                window_size=8
            )

        )



    def analyze(
        self,
        path,
    ) -> dict:
        """
        Analyze a Capture project file.
        """


        file_path = Path(
            path
        )


        if not file_path.exists():

            raise FileNotFoundError(
                file_path
            )


        data = file_path.read_bytes()



        detection = self.detector.detect(
            data
        )



        return {

            "file": str(file_path),

            "size": len(data),

            "signature_count": detection.get(
                "count",
                0,
            ),

            "signatures": detection.get(
                "signatures",
                [],
            ),

        }