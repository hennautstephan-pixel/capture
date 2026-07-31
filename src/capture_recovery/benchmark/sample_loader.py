"""
Sample loader.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


class SampleLoader:
    """
    Discovers Capture sample projects.

    The loader is intentionally simple: it only discovers
    `.c2p` files. It never opens or analyses them.
    """

    def __init__(
        self,
        root: Path | str,
    ) -> None:

        self._root = Path(root)

    @property
    def root(self) -> Path:
        """
        Root directory containing sample projects.
        """
        return self._root

    def exists(self) -> bool:
        """
        Returns True if the sample directory exists.
        """

        return self._root.exists()

    def load(self) -> list[Path]:
        """
        Returns every .c2p file found recursively.

        The returned list is always sorted to ensure
        deterministic benchmark execution.
        """

        if not self.exists():
            return []

        return sorted(
            path
            for path in self._root.rglob("*.c2p")
            if path.is_file()
        )

    def count(self) -> int:
        """
        Returns the number of discovered sample projects.
        """

        return len(self.load())

    def __iter__(self) -> Iterator[Path]:
        """
        Iterate over sample projects.

        Example
        -------
        for sample in loader:
            ...
        """

        return iter(self.load())

    def __len__(self) -> int:
        """
        Number of discovered sample projects.
        """

        return self.count()