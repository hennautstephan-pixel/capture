"""
Capture reader.

Loads Capture project files
for recovery analysis.
"""

from __future__ import annotations

import json
from pathlib import Path


class CaptureReader:
    """
    Reads Capture project data.
    """

    def read(
        self,
        path,
    ) -> dict:
        """
        Read a Capture file.

        Currently supports JSON based
        recovery files.
        """

        file_path = Path(
            path,
        )


        if not file_path.exists():

            raise FileNotFoundError(
                str(file_path)
            )


        with open(
            file_path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(
                file,
            )


    def read_bytes(
        self,
        path,
    ) -> bytes:
        """
        Read raw binary content.
        """

        file_path = Path(
            path,
        )

        return file_path.read_bytes()