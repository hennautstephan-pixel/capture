"""
Capture signature analyzer.

Analyzes repeated binary signatures
inside Capture project files.
"""

from __future__ import annotations

from pathlib import Path


from .capture_signature_detector import (
    CaptureSignatureDetector,
)



class CaptureSignatureAnalyzer:
    """
    High level signature analysis.
    """



    def __init__(
        self,
        detector=None,
    ):

        self.detector = (

            detector

            if detector is not None

            else CaptureSignatureDetector()

        )



    def analyze(
        self,
        path,
    ) -> dict:
        """
        Analyze signatures from a file.
        """


        path = Path(
            path
        )


        if not path.exists():

            raise FileNotFoundError(
                path
            )


        data = path.read_bytes()



        signatures = self.detector.detect(
            data
        )



        return {

            "file": str(path),

            "size": len(data),

            "signature_count": signatures.get(
                "count",
                0,
            ),

            "signatures": signatures.get(
                "signatures",
                [],
            ),

        }