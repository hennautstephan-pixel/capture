"""
Header scanner.

Scans binary buffers looking for known Capture header signatures.
This class is intentionally generic and independent from the parser.

Future versions will support:

- fuzzy matching
- partial signatures
- checksum validation
- alignment heuristics
- corrupted header recovery
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class HeaderSignature:
    """
    Binary header signature.
    """

    name: str
    pattern: bytes
    priority: int = 100

    @property
    def size(self) -> int:
        return len(self.pattern)


@dataclass(frozen=True, slots=True)
class ScanResult:
    """
    One header occurrence.
    """

    offset: int
    signature: HeaderSignature
    confidence: float = 1.0

    @property
    def end_offset(self) -> int:
        return self.offset + self.signature.size


class HeaderScanner:
    """
    Binary header scanner.

    The scanner searches a binary buffer for registered header signatures.

    It does not interpret the data.
    """

    def __init__(self) -> None:
        self._signatures: list[HeaderSignature] = []

    @property
    def signatures(self) -> tuple[HeaderSignature, ...]:
        return tuple(self._signatures)

    def register(
        self,
        signature: HeaderSignature,
    ) -> None:
        """
        Register a signature.
        """

        if signature not in self._signatures:
            self._signatures.append(signature)

            self._signatures.sort(
                key=lambda s: (-s.priority, -s.size)
            )

    def register_many(
        self,
        signatures: Iterable[HeaderSignature],
    ) -> None:
        """
        Register multiple signatures.
        """

        for signature in signatures:
            self.register(signature)

    def clear(self) -> None:
        """
        Remove every registered signature.
        """

        self._signatures.clear()

    def scan(
        self,
        data: bytes,
    ) -> list[ScanResult]:
        """
        Scan an entire binary buffer.

        Results are sorted by offset.
        """

        if not data:
            return []

        results: list[ScanResult] = []

        for signature in self._signatures:

            position = 0

            while True:

                position = data.find(
                    signature.pattern,
                    position,
                )

                if position < 0:
                    break

                results.append(
                    ScanResult(
                        offset=position,
                        signature=signature,
                    )
                )

                position += 1

        results.sort(
            key=lambda result: result.offset
        )

        return results

    def first(
        self,
        data: bytes,
    ) -> ScanResult | None:
        """
        Return the first detected header.
        """

        results = self.scan(data)

        if results:
            return results[0]

        return None

    def nearest(
        self,
        data: bytes,
        offset: int,
    ) -> ScanResult | None:
        """
        Return the nearest detected header.
        """

        results = self.scan(data)

        if not results:
            return None

        return min(
            results,
            key=lambda result: abs(
                result.offset - offset
            ),
        )

    def between(
        self,
        data: bytes,
        start: int,
        end: int,
    ) -> list[ScanResult]:
        """
        Return headers located inside a range.
        """

        return [
            result
            for result in self.scan(data)
            if start <= result.offset <= end
        ]

    def count(
        self,
        data: bytes,
    ) -> int:
        """
        Count detected headers.
        """

        return len(self.scan(data))

    def has_header(
        self,
        data: bytes,
    ) -> bool:
        """
        True if at least one header is found.
        """

        return self.first(data) is not None

    def __len__(self) -> int:
        return len(self._signatures)

    def __iter__(self):
        return iter(self._signatures)