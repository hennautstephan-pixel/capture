"""
Capture Recovery

BinaryReader

Robust binary reader with random access support.
"""

from __future__ import annotations

import struct
from pathlib import Path
from typing import BinaryIO, Iterator


class BinaryReader:
    """
    Robust binary reader.

    Can be used either as a context manager:

        with BinaryReader("file.bin") as reader:
            ...

    or manually:

        reader = BinaryReader("file.bin")
        reader.open()
        ...
        reader.close()
    """

    def __init__(self, path: str | Path):

        self.path = Path(path)

        if not self.path.is_file():
            raise FileNotFoundError(
                f"File not found: {self.path}"
            )

        self.file: BinaryIO | None = None
        self.size = self.path.stat().st_size

    # ------------------------------------------------------------------
    # Open / Close
    # ------------------------------------------------------------------

    def open(self) -> "BinaryReader":

        if self.file is None:
            self.file = self.path.open("rb")

        return self

    def close(self) -> None:

        if self.file is not None:
            self.file.close()
            self.file = None

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> "BinaryReader":

        return self.open()

    def __exit__(self, exc_type, exc_value, traceback) -> None:

        self.close()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _file(self) -> BinaryIO:
        """
        Returns the opened file.

        Raises
        ------
        RuntimeError
            If the reader has not been opened.
        """

        if self.file is None:
            raise RuntimeError(
                "BinaryReader is not open.\n"
                "Use:\n"
                "    with BinaryReader(path) as reader:\n"
                "or:\n"
                "    reader.open()"
            )

        return self.file

    # ------------------------------------------------------------------
    # Position
    # ------------------------------------------------------------------

    def tell(self) -> int:

        return self._file().tell()

    def seek(self, offset: int) -> None:

        if offset < 0:
            raise ValueError("Negative offset.")

        self._file().seek(offset)

    def skip(self, length: int) -> None:

        self._file().seek(length, 1)

    # ------------------------------------------------------------------
    # EOF
    # ------------------------------------------------------------------

    @property
    def eof(self) -> bool:

        return self.tell() >= self.size

    @property
    def remaining(self) -> int:

        return self.size - self.tell()

    def can_read(self, length: int) -> bool:

        return self.remaining >= length

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def read(self, length: int) -> bytes:
        """
        Strict read.

        Raises EOFError if the requested number of bytes
        cannot be read.
        """

        if length < 0:
            raise ValueError("Negative length.")

        if not self.can_read(length):
            raise EOFError("End of file reached.")

        data = self._file().read(length)

        if len(data) != length:
            raise EOFError("Incomplete read.")

        return data

    def read_safe(self, length: int) -> bytes:
        """
        Safe read.

        Returns fewer bytes if EOF is reached.
        """

        if length <= 0:
            return b""

        if self.remaining <= 0:
            return b""

        return self._file().read(min(length, self.remaining))

    # ------------------------------------------------------------------
    # Integer readers
    # ------------------------------------------------------------------

    def read_u8(self) -> int:

        return int.from_bytes(self.read(1), "little")

    def read_u16(self) -> int:

        return struct.unpack("<H", self.read(2))[0]

    def read_u32(self) -> int:

        return struct.unpack("<I", self.read(4))[0]

    def read_u64(self) -> int:

        return struct.unpack("<Q", self.read(8))[0]

    # ------------------------------------------------------------------
    # Random access
    # ------------------------------------------------------------------

    def read_u32_at(self, offset: int) -> int:

        pos = self.tell()

        self.seek(offset)

        value = self.read_u32()

        self.seek(pos)

        return value

    # ------------------------------------------------------------------
    # Strings
    # ------------------------------------------------------------------

    def read_string(
        self,
        length: int,
        encoding: str = "utf-8",
    ) -> str:

        return self.read(length).decode(
            encoding,
            errors="replace",
        )

    def read_cstring(
        self,
        encoding: str = "utf-8",
    ) -> str:

        chars = bytearray()

        while self.can_read(1):

            c = self.read(1)

            if c == b"\x00":
                break

            chars.extend(c)

        return chars.decode(
            encoding,
            errors="replace",
        )

    # ------------------------------------------------------------------
    # Peek
    # ------------------------------------------------------------------

    def peek(self, length: int) -> bytes:

        pos = self.tell()

        data = self.read_safe(length)

        self.seek(pos)

        return data

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def find(
        self,
        pattern: bytes,
        start: int = 0,
    ) -> int:

        pos = self.tell()

        self.seek(start)

        data = self._file().read()

        self.seek(pos)

        idx = data.find(pattern)

        if idx == -1:
            return -1

        return start + idx

    def find_all(
        self,
        pattern: bytes,
    ) -> Iterator[int]:

        pos = self.tell()

        self.seek(0)

        data = self._file().read()

        self.seek(pos)

        start = 0

        while True:

            idx = data.find(pattern, start)

            if idx == -1:
                break

            yield idx

            start = idx + 1

    # ------------------------------------------------------------------
    # Hexdump
    # ------------------------------------------------------------------

    def hexdump(
        self,
        offset: int,
        length: int = 64,
    ) -> str:

        pos = self.tell()

        self.seek(offset)

        data = self.read_safe(length)

        self.seek(pos)

        lines: list[str] = []

        for i in range(0, len(data), 16):

            chunk = data[i:i + 16]

            hex_part = " ".join(
                f"{b:02X}"
                for b in chunk
            )

            ascii_part = "".join(
                chr(b) if 32 <= b <= 126 else "."
                for b in chunk
            )

            lines.append(
                f"{offset + i:08X}  "
                f"{hex_part:<47}  "
                f"{ascii_part}"
            )

        return "\n".join(lines)

    def dump_around(
        self,
        offset: int,
        before: int = 32,
        after: int = 32,
    ) -> str:

        start = max(0, offset - before)

        return self.hexdump(
            start,
            before + after,
        )

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def __len__(self) -> int:

        return self.size

    def __repr__(self) -> str:

        state = "open" if self.file is not None else "closed"

        return (
            f"{self.__class__.__name__}("
            f"path='{self.path}', "
            f"size={self.size}, "
            f"state='{state}')"
        )