"""
capture_recovery.reverse.hex_inspector

Generic hexadecimal inspector used during reverse engineering.

This module intentionally performs no Capture-specific parsing.
It exposes multiple interpretations of the binary data and is
intended to be reused by BinaryMap and BinaryReport.
"""

from __future__ import annotations

from dataclasses import dataclass
import struct


_PRINTABLE = frozenset(range(32, 127))


@dataclass(slots=True, frozen=True)
class HexRow:
    """One row of hexadecimal inspection."""

    offset: int
    raw: bytes
    hex: str
    ascii: str
    u32_le: int | None
    f32_le: float | None


class HexInspector:
    """Inspect binary buffers without interpreting their meaning."""

    @classmethod
    def inspect(
        cls,
        data: bytes | bytearray | memoryview,
        *,
        width: int = 16,
    ) -> list[HexRow]:
        """
        Produce a structured hexadecimal view of *data*.

        Parameters
        ----------
        data
            Binary buffer to inspect.

        width
            Number of bytes per output row.

        Returns
        -------
        list[HexRow]
        """

        if width <= 0:
            raise ValueError("width must be > 0")

        if isinstance(data, memoryview):
            buffer = data.tobytes()
        else:
            buffer = bytes(data)

        rows: list[HexRow] = []

        for offset in range(0, len(buffer), width):

            chunk = buffer[offset : offset + width]

            hex_string = " ".join(f"{b:02X}" for b in chunk)

            ascii_string = "".join(
                chr(b) if b in _PRINTABLE else "."
                for b in chunk
            )

            if len(chunk) >= 4:
                u32_value = struct.unpack("<I", chunk[:4])[0]
                f32_value = struct.unpack("<f", chunk[:4])[0]
            else:
                u32_value = None
                f32_value = None

            rows.append(
                HexRow(
                    offset=offset,
                    raw=chunk,
                    hex=hex_string,
                    ascii=ascii_string,
                    u32_le=u32_value,
                    f32_le=f32_value,
                )
            )

        return rows