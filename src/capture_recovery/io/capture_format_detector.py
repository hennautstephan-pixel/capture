"""
Capture format detector.

Detects Capture file types from
binary signatures.
"""

from __future__ import annotations

from pathlib import Path


class CaptureFormatDetector:
    """
    Detect Capture file format.
    """

    SIGNATURES = {

        "capture_binary": (
            b"CAPTURE",
        ),

        "json": (
            b"{",
        ),

    }


    def detect(
        self,
        path,
    ) -> str:
        """
        Detect format from file header.
        """

        file_path = Path(
            path,
        )

        header = file_path.read_bytes()[:32]


        for name, signatures in self.SIGNATURES.items():

            for signature in signatures:

                if header.startswith(
                    signature,
                ):

                    return name


        return "unknown"