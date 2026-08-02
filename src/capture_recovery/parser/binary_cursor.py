from __future__ import annotations

import struct


class BinaryCursor:
    """
    Sequential binary reader.

    Provides convenient methods for reading primitive
    values from a byte buffer.
    """

    def __init__(
        self,
        data: bytes,
    ) -> None:

        self._data = data

        self._position = 0

    @property
    def size(self) -> int:
        return len(self._data)

    @property
    def position(self) -> int:
        return self._position

    @property
    def remaining(self) -> int:
        return self.size - self._position

    @property
    def eof(self) -> bool:
        return self._position >= self.size

    def tell(self) -> int:
        return self._position

    def seek(
        self,
        position: int,
    ) -> None:

        if not 0 <= position <= self.size:
            raise ValueError(
                "Position outside buffer."
            )

        self._position = position

    def skip(
        self,
        count: int,
    ) -> None:

        self.seek(
            self._position + count,
        )

    def align(
        self,
        alignment: int,
    ) -> None:

        if alignment <= 0:
            raise ValueError(
                "Alignment must be positive."
            )

        remainder = self._position % alignment

        if remainder:
            self.skip(
                alignment - remainder,
            )

    def peek(
        self,
        count: int,
    ) -> bytes:

        end = min(
            self._position + count,
            self.size,
        )

        return self._data[
            self._position:end
        ]

    def read_bytes(
        self,
        count: int,
    ) -> bytes:

        data = self.peek(
            count,
        )

        self.skip(
            len(data),
        )

        return data

    def read_u8(self) -> int:
        return self.read_bytes(1)[0]

    def read_u16(self) -> int:
        return int.from_bytes(
            self.read_bytes(2),
            "little",
        )

    def read_u32(self) -> int:
        return int.from_bytes(
            self.read_bytes(4),
            "little",
        )

    def read_i32(self) -> int:
        return int.from_bytes(
            self.read_bytes(4),
            "little",
            signed=True,
        )

    def read_float(self) -> float:
        return struct.unpack(
            "<f",
            self.read_bytes(4),
        )[0]

    def read_string(
        self,
        length: int,
        *,
        encoding: str = "utf-8",
    ) -> str:

        return (
            self.read_bytes(length)
            .split(b"\x00")[0]
            .decode(
                encoding,
                errors="ignore",
            )
        )