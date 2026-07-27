"""
Capture Recovery

Pattern Analyzer

Détecte les blocs binaires répétés et les ajoute au rapport.
"""

from __future__ import annotations

from collections import defaultdict

from ..binary_reader import BinaryReader
from ..models import (
    Finding,
    FindingType,
    Report,
    Severity,
)


class PatternAnalyzer:
    """Détecte les motifs binaires répétés."""

    def __init__(
        self,
        pattern_sizes: tuple[int, ...] = (32, 64, 128),
        min_occurrences: int = 3,
    ) -> None:

        self.pattern_sizes = pattern_sizes
        self.min_occurrences = min_occurrences

    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:
        """
        Recherche les blocs binaires identiques apparaissant plusieurs fois
        dans le fichier.
        """

        for size in self.pattern_sizes:

            reader.seek(0)

            patterns: dict[bytes, list[int]] = defaultdict(list)

            while reader.can_read(size):

                offset = reader.tell()
                block = reader.read(size)

                patterns[block].append(offset)

            for block, offsets in patterns.items():

                if len(offsets) < self.min_occurrences:
                    continue

                finding = Finding(
                    offset=offsets[0],
                    length=size,
                    category=FindingType.PATTERN,
                    description=(
                        f"Repeated binary pattern "
                        f"({len(offsets)} occurrences)"
                    ),
                    value=", ".join(
                        hex(offset)
                        for offset in offsets[:10]
                    ),
                    severity=Severity.INFO,
                )

                report.add_finding(finding)