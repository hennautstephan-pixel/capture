from __future__ import annotations

from dataclasses import dataclass

from .corpus_builder import (
    CorpusEntry,
)


@dataclass(slots=True, frozen=True)
class Difference:
    """
    One difference between two Capture samples.
    """

    field: str

    left: object

    right: object


@dataclass(slots=True, frozen=True)
class CorpusDiff:
    """
    Comparison result between two corpus entries.
    """

    left: CorpusEntry

    right: CorpusEntry

    differences: tuple[Difference, ...]

    @property
    def identical(self) -> bool:
        return not self.differences

    @property
    def difference_count(self) -> int:
        return len(self.differences)


class CorpusDiffer:
    """
    Compare two corpus entries.
    """

    def compare(
        self,
        left: CorpusEntry,
        right: CorpusEntry,
    ) -> CorpusDiff:

        differences: list[Difference] = []

        self._compare(
            differences,
            "format",
            left.format,
            right.format,
        )

        self._compare(
            differences,
            "size",
            left.size,
            right.size,
        )

        self._compare(
            differences,
            "compressed_size",
            left.compressed_size,
            right.compressed_size,
        )

        self._compare(
            differences,
            "decompressed_size",
            left.decompressed_size,
            right.decompressed_size,
        )

        self._compare(
            differences,
            "stream_offset",
            left.stream_offset,
            right.stream_offset,
        )

        self._compare(
            differences,
            "sha256",
            left.sha256,
            right.sha256,
        )

        return CorpusDiff(
            left=left,
            right=right,
            differences=tuple(differences),
        )

    @staticmethod
    def _compare(
        differences: list[Difference],
        field: str,
        left: object,
        right: object,
    ) -> None:

        if left != right:

            differences.append(
                Difference(
                    field=field,
                    left=left,
                    right=right,
                )
            )