"""
Capture Recovery

Pointer Analyzer

Détecte les valeurs uint32 pouvant représenter
des offsets internes au fichier.
"""

from __future__ import annotations

from ..binary_reader import BinaryReader
from ..models import (
    Finding,
    FindingType,
    Report,
    Severity,
)

from .numbers import NumberAnalyzer


class PointerAnalyzer:
    """Détecte les pointeurs internes plausibles."""

    def __init__(
        self,
        alignment: int = 4,
    ) -> None:

        self.alignment = alignment

    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:
        """
        Recherche les uint32 pouvant représenter
        des offsets internes au fichier.
        """

        numbers = NumberAnalyzer(reader)

        for offset in range(
            0,
            reader.size - 4,
            self.alignment,
        ):

            value = numbers.read_u32(offset)

            # Valeur invalide
            if value == 0:
                continue

            if not numbers.is_plausible_pointer(value):
                continue

            reader.seek(value)
            target = reader.read(8)

            score = self._score(target)

            if score < 2:
                continue

            finding = Finding(
                offset=offset,
                length=4,
                category=FindingType.POINTER,
                description=f"Possible pointer -> 0x{value:08X}",
                value=value,
                severity=Severity.INFO,
            )

            report.add_finding(finding)

    @staticmethod
    def _score(data: bytes) -> int:
        """
        Attribue un score de plausibilité à la cible.
        """

        score = 0

        printable = sum(
            32 <= byte <= 126
            for byte in data
        )

        if printable >= 4:
            score += 2

        if any(data):
            score += 1

        return score