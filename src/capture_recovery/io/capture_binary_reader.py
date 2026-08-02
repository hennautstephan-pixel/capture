"""
Capture binary reader.

Reads raw Capture binary files.
"""

from __future__ import annotations

from pathlib import Path


class CaptureBinaryReader:
    """
    Read raw binary Capture project files.
    """

    def read(
        self,
        path: str | Path,
    ) -> bytes:
        """
        Read the complete binary content of a Capture file.
        """

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(str(file_path))

        return file_path.read_bytes()

    def read_header(
        self,
        path: str | Path,
        *,
        size: int = 32,
    ) -> bytes:
        """
        Read the beginning of a Capture file.

        The default size is provisional and will be
        replaced once the real header layout is known.
        """

        return self.read(path)[:size]

    def read_footer(
        self,
        path: str | Path,
        *,
        size: int = 32,
    ) -> bytes:
        """
        Read the end of a Capture file.
        """

        data = self.read(path)

        return data[-size:] if len(data) >= size else data

    def read_stream(
        self,
        path: str | Path,
        *,
        header_size: int = 32,
        footer_size: int = 32,
    ) -> bytes:
        """
        Read the payload section of a Capture file.

        This implementation currently uses heuristic
        offsets and will be replaced by the real parser.
        """

        data = self.read(path)

        if len(data) <= header_size + footer_size:
            return b""

        return data[header_size:-footer_size]