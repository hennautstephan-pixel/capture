"""
Capture reader.

Loads Capture project files
for recovery analysis.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .capture_binary_reader import CaptureBinaryReader
from .capture_format_detector import CaptureFormatDetector


class CaptureReader:
    """
    High-level Capture project reader.

    This class delegates low-level binary reading
    and format detection to specialized components.
    """

    def __init__(self) -> None:

        self._binary_reader = CaptureBinaryReader()

        self._format_detector = CaptureFormatDetector()

    def detect_format(
        self,
        path: str | Path,
    ) -> str:
        """
        Detect the Capture file format.
        """

        return self._format_detector.detect(path)

    def read(
        self,
        path: str | Path,
    ) -> dict[str, Any]:
        """
        Read a supported Capture project.

        JSON recovery projects are parsed.
        Binary Capture projects are returned
        as raw bytes inside a dictionary until
        a dedicated parser is available.
        """

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(str(file_path))

        file_format = self.detect_format(file_path)

        if file_format == "json":

            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        return {
            "format": file_format,
            "data": self._binary_reader.read(file_path),
        }

    def read_bytes(
        self,
        path: str | Path,
    ) -> bytes:
        """
        Read the raw binary content of a file.
        """

        return self._binary_reader.read(path)