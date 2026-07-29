"""
String extraction utilities.

Scans binary buffers and extracts printable strings.

Supported encodings
-------------------
- ASCII
- UTF-16 Little Endian
- UTF-16 Big Endian
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

__all__ = [
    "ExtractedString",
    "StringScanner",
]


PRINTABLE_MIN = 32
PRINTABLE_MAX = 126


@dataclass(slots=True, frozen=True)
class ExtractedString:
    offset: int
    length: int
    encoding: str
    text: str


class StringScanner:
    @staticmethod
    def scan(
        data: bytes | bytearray | memoryview,
        *,
        minimum_length: int = 4,
    ) -> list[ExtractedString]:

        if minimum_length < 1:
            raise ValueError("minimum_length must be >= 1")

        if isinstance(data, memoryview):
            data = data.tobytes()
        elif isinstance(data, bytearray):
            data = bytes(data)

        results: list[ExtractedString] = []

        results.extend(
            StringScanner._scan_ascii(
                data,
                minimum_length,
            )
        )

        results.extend(
            StringScanner._scan_utf16_le(
                data,
                minimum_length,
            )
        )

        results.extend(
            StringScanner._scan_utf16_be(
                data,
                minimum_length,
            )
        )

        results.sort(key=lambda s: (s.offset, s.encoding))

        return results

    @staticmethod
    def _is_printable(value: int) -> bool:
        return PRINTABLE_MIN <= value <= PRINTABLE_MAX

    @staticmethod
    def _scan_ascii(
        data: bytes,
        minimum_length: int,
    ) -> Iterable[ExtractedString]:

        start = None
        chars: list[str] = []

        for index, value in enumerate(data):

            if StringScanner._is_printable(value):

                if start is None:
                    start = index

                chars.append(chr(value))

            else:

                if start is not None and len(chars) >= minimum_length:
                    yield ExtractedString(
                        offset=start,
                        length=len(chars),
                        encoding="ascii",
                        text="".join(chars),
                    )

                start = None
                chars.clear()

        if start is not None and len(chars) >= minimum_length:
            yield ExtractedString(
                offset=start,
                length=len(chars),
                encoding="ascii",
                text="".join(chars),
            )

    @staticmethod
    def _scan_utf16_le(
        data: bytes,
        minimum_length: int,
    ) -> Iterable[ExtractedString]:

        i = 0
        size = len(data)

        while i + 1 < size:

            start = i
            chars: list[str] = []

            while (
                i + 1 < size
                and data[i + 1] == 0
                and StringScanner._is_printable(data[i])
            ):
                chars.append(chr(data[i]))
                i += 2

            if len(chars) >= minimum_length:
                yield ExtractedString(
                    offset=start,
                    length=len(chars),
                    encoding="utf-16le",
                    text="".join(chars),
                )
                continue

            i = start + 1

    @staticmethod
    def _scan_utf16_be(
        data: bytes,
        minimum_length: int,
    ) -> Iterable[ExtractedString]:

        i = 0
        size = len(data)

        while i + 1 < size:

            start = i
            chars: list[str] = []

            while (
                i + 1 < size
                and data[i] == 0
                and StringScanner._is_printable(data[i + 1])
            ):
                chars.append(chr(data[i + 1]))
                i += 2

            if len(chars) >= minimum_length:
                yield ExtractedString(
                    offset=start,
                    length=len(chars),
                    encoding="utf-16be",
                    text="".join(chars),
                )
                continue

            i = start + 1