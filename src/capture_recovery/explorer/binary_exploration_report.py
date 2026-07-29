"""
Result object returned by binary exploration.

The report aggregates every structure produced while analysing a C2P
file before any semantic reconstruction occurs.
"""

from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.binary.binary_container import BinaryContainer
from capture_recovery.binary.binary_graph import BinaryGraph
from capture_recovery.binary.binary_index import BinaryIndex
from capture_recovery.binary.decode_coverage import DecodeCoverage


@dataclass(slots=True, frozen=True)
class BinaryExplorationReport:
    """
    Immutable result of a binary exploration.
    """

    container: BinaryContainer
    index: BinaryIndex
    graph: BinaryGraph
    coverage: DecodeCoverage

    #
    # File metadata
    #
    sha256: str

    @property
    def object_count(self) -> int:
        """
        Number of binary objects discovered.
        """
        return self.index.count()

    @property
    def reference_count(self) -> int:
        """
        Number of binary references discovered.
        """
        return len(self.graph)

    @property
    def section_count(self) -> int:
        """
        Number of sections detected.
        """
        return len(self.container.sections)