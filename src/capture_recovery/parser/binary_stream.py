"""
capture_recovery.parser.binary_stream

Abstraction de lecture binaire utilisée par tous les parseurs C2P.

Auteur : Capture Recovery Project
"""

from __future__ import annotations

import struct
import uuid
from pathlib import Path
from typing import Union


class BinaryStream:
    """
    Binary reader with little-endian helpers.

    The stream is read-only.
    """

    def __init__(self, data: bytes):
        self._buffer = memoryview(data)
        self._position = 0

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def from_file(cls, filename: Union[str, Path]) -> "BinaryStream":
        return cls(Path(filename).read_bytes())

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def size(self) -> int:
        return len(self._buffer)

    @property
    def position(self) -> int:
        return self._position

    @property
    def remaining(self) -> int:
        return self.size - self._position

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def eof(self) -> bool:
        return self._position >= self.size

    def tell(self) -> int:
        return self._position

    def seek(self, offset: int) -> None:
        if not 0 <= offset <= self.size:
            raise ValueError(f"Invalid offset {offset}")
        self._position = offset

    def skip(self, length: int) -> None:
        self.seek(self._position + length)

    # ------------------------------------------------------------------
    # Raw access
    # ------------------------------------------------------------------

    def read(self, length: int) -> bytes:
        if length < 0:
            raise ValueError("length must be >= 0")

        if self._position + length > self.size:
            raise EOFError("Unexpected end of stream")

        data = self._buffer[
            self._position:self._position + length
        ].tobytes()

        self._position += length
        return data

    def peek(self, length: int) -> bytes:
        if length < 0:
            raise ValueError("length must be >= 0")

        if self._position + length > self.size:
            raise EOFError("Unexpected end of stream")

        return self._buffer[
            self._position:self._position + length
        ].tobytes()

    # ------------------------------------------------------------------
    # Integer readers
    # ------------------------------------------------------------------

    def u8(self) -> int:
        return struct.unpack("<B", self.read(1))[0]

    def i8(self) -> int:
        return struct.unpack("<b", self.read(1))[0]

    def u16(self) -> int:
        return struct.unpack("<H", self.read(2))[0]

    def i16(self) -> int:
        return struct.unpack("<h", self.read(2))[0]

    def u32(self) -> int:
        return struct.unpack("<I", self.read(4))[0]

    def i32(self) -> int:
        return struct.unpack("<i", self.read(4))[0]

    def u64(self) -> int:
        return struct.unpack("<Q", self.read(8))[0]

    def i64(self) -> int:
        return struct.unpack("<q", self.read(8))[0]

    # ------------------------------------------------------------------
    # Floating point
    # ------------------------------------------------------------------

    def f32(self) -> float:
        return struct.unpack("<f", self.read(4))[0]

    def f64(self) -> float:
        return struct.unpack("<d", self.read(8))[0]

    # ------------------------------------------------------------------
    # UUID
    # ------------------------------------------------------------------

    def uuid(self) -> uuid.UUID:
        return uuid.UUID(bytes_le=self.read(16))

    # ------------------------------------------------------------------
    # Strings
    # ------------------------------------------------------------------

    def cstring(
        self,
        encoding: str = "utf-8",
        errors: str = "ignore",
    ) -> str:
        start = self._position

        while not self.eof():
            if self._buffer[self._position] == 0:
                break
            self._position += 1

        if self.eof():
            raise EOFError("Unterminated C string")

        data = self._buffer[start:self._position].tobytes()

        self._position += 1

        return data.decode(encoding, errors)

    def fixed_string(
        self,
        length: int,
        encoding: str = "utf-8",
        errors: str = "ignore",
    ) -> str:
        return self.read(length).decode(encoding, errors)

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def align(self, alignment: int) -> None:
        if alignment <= 0:
            raise ValueError("alignment must be > 0")

        new_position = (
            (self._position + alignment - 1)
            // alignment
        ) * alignment

        self.seek(new_position)

    def slice(self, offset: int, length: int) -> bytes:
        if offset < 0:
            raise ValueError("offset must be >= 0")

        if offset + length > self.size:
            raise EOFError("Slice outside stream")

        return self._buffer[offset:offset + length].tobytes()

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return (
            f"<BinaryStream "
            f"position={self.position} "
            f"size={self.size}>"
        )