"""
Capture format detector.

Detects Capture file types from
binary signatures.
"""

from __future__ import annotations

from pathlib import Path


class CaptureFormatDetector:
    """
    Detect the format of a Capture project.
    """

    SIGNATURES = {
        "capture_binary": (
            b"CAPTURE",
        ),
        "json": (
            b"{",
        ),
    }

    UNKNOWN = "unknown"

    def detect(
        self,
        path: str | Path,
    ) -> str:
        """
        Detect a file format from its header.
        """

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(str(file_path))

        header = file_path.read_bytes()[:32]

        return self.detect_bytes(header)

    def detect_bytes(
        self,
        data: bytes,
    ) -> str:
        """
        Detect a format directly from binary data.
        """

        for name, signatures in self.SIGNATURES.items():

            for signature in signatures:

                if data.startswith(signature):
                    return name

        return self.UNKNOWN

    def is_supported(
        self,
        path: str | Path,
    ) -> bool:
        """
        Return True if the file format is recognised.
        """

        return self.detect(path) != self.UNKNOWN