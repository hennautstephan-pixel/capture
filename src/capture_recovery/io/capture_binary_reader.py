"""
Capture binary reader.

Reads raw Capture binary files.
"""

from __future__ import annotations

from pathlib import Path


class CaptureBinaryReader:
    """
    Reads binary Capture data.
    """

    def read(
        self,
        path,
    ) -> bytes:
        """
        Return raw binary content.
        """

        file_path = Path(
            path,
        )

        return file_path.read_bytes()