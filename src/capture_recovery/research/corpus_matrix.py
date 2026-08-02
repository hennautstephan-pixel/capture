from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .corpus_diff import (
    CorpusDiff,
    CorpusDifference,
)


@dataclass(slots=True, frozen=True)
class MatrixEntry:
    """
    Comparison between two Capture projects.
    """

    left: Path

    right: Path

    difference: CorpusDifference

    @property
    def identical(self) -> bool:
        return self.difference.decompressed_equal

    @property
    def changed_region_count(self) -> int:
        return len(self.difference.changed_regions)


class CorpusMatrix:
    """
    Symmetric matrix of project comparisons.
    """

    def __init__(self) -> None:

        self._entries: dict[
            tuple[Path, Path],
            MatrixEntry,
        ] = {}

        self._projects: set[Path] = set()

    @staticmethod
    def _key(
        left: Path,
        right: Path,
    ) -> tuple[Path, Path]:

        if left.name <= right.name:
            return left, right

        return right, left

    def add(
        self,
        entry: MatrixEntry,
    ) -> None:

        self._projects.add(entry.left)
        self._projects.add(entry.right)

        self._entries[
            self._key(
                entry.left,
                entry.right,
            )
        ] = entry

    def get(
        self,
        left: Path,
        right: Path,
    ) -> MatrixEntry | None:

        return self._entries.get(
            self._key(
                left,
                right,
            )
        )

    @property
    def projects(self) -> list[Path]:

        return sorted(self._projects)

    @property
    def project_count(self) -> int:

        return len(self._projects)

    @property
    def entries(self) -> list[MatrixEntry]:

        return sorted(
            self._entries.values(),
            key=lambda e: (
                e.left.name,
                e.right.name,
            ),
        )

    def identical_pairs(
        self,
    ) -> list[MatrixEntry]:

        return [
            entry
            for entry in self.entries
            if entry.identical
        ]

    def different_pairs(
        self,
    ) -> list[MatrixEntry]:

        return [
            entry
            for entry in self.entries
            if not entry.identical
        ]


class CorpusMatrixAnalyzer:
    """
    Compare every Capture project in a corpus.
    """

    def __init__(
        self,
        diff: CorpusDiff | None = None,
    ) -> None:

        self._diff = diff or CorpusDiff()

    def analyze(
        self,
        directory: str | Path,
        pattern: str = "*.c2p",
    ) -> CorpusMatrix:

        directory = Path(directory)

        projects = sorted(
            directory.glob(pattern)
        )

        matrix = CorpusMatrix()

        #
        # Enregistrer tous les projets, même si aucune
        # comparaison n'est créée.
        #
        matrix._projects.update(projects)

        for index, left in enumerate(projects):

            for right in projects[index + 1:]:

                matrix.add(
                    MatrixEntry(
                        left=left,
                        right=right,
                        difference=self._diff.compare(
                            left,
                            right,
                        ),
                    )
                )

        return matrix