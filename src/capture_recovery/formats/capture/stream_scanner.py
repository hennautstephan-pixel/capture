from __future__ import annotations

from collections.abc import Iterable


class CaptureStreamScanner:
    """
    Locate candidate compressed streams inside a Capture (.c2p) file.

    The scanner only detects known binary signatures.
    It does not validate or decompress streams.
    """

    DEFAULT_SIGNATURES: tuple[bytes, ...] = (
        b"\x78\x01",
        b"\x78\x5E",
        b"\x78\x9C",
        b"\x78\xDA",
    )

    def __init__(
        self,
        signatures: Iterable[bytes] | None = None,
    ) -> None:

        if signatures is None:
            signatures = self.DEFAULT_SIGNATURES

        self._signatures = tuple(signatures)

    @property
    def signatures(self) -> tuple[bytes, ...]:
        return self._signatures

    def find(
        self,
        data: bytes,
    ) -> list[int]:
        """
        Return every offset matching one of the known signatures.
        """

        offsets: list[int] = []

        if len(data) < 2:
            return offsets

        limit = len(data) - 1

        for offset in range(limit):

            if data[offset:offset + 2] in self._signatures:
                offsets.append(offset)

        return offsets

    def first(
        self,
        data: bytes,
    ) -> int | None:
        """
        Return the first matching offset.
        """

        matches = self.find(data)

        if matches:
            return matches[0]

        return None