"""
Binary explorer.

This service is the entry point of the reverse engineering pipeline.
It creates an initial BinaryExplorationReport from a Capture project
without attempting any semantic decoding.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from capture_recovery.binary.binary_container import BinaryContainer
from capture_recovery.binary.binary_graph import BinaryGraph
from capture_recovery.binary.binary_index import BinaryIndex
from capture_recovery.binary.decode_coverage import DecodeCoverage

from .binary_exploration_report import BinaryExplorationReport


class BinaryExplorer:
    """
    Explore a Capture binary file.

    The first implementation gathers basic information.
    Future versions will progressively populate the binary index,
    graph and coverage.
    """

    def explore(self, path: str | Path) -> BinaryExplorationReport:
        """
        Explore a Capture binary file.

        Parameters
        ----------
        path:
            Path to the .c2p file.

        Returns
        -------
        BinaryExplorationReport
        """

        file_path = Path(path)

        data = file_path.read_bytes()

        sha256 = hashlib.sha256(data).hexdigest()

        container = BinaryContainer(
            path=str(file_path),
            file_size=len(data),
            sections=(),
        )

        return BinaryExplorationReport(
            container=container,
            index=BinaryIndex(objects={}),
            graph=BinaryGraph(),
            coverage=DecodeCoverage(),
            sha256=sha256,
        )