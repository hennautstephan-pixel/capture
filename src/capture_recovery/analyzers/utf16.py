"""
Capture Recovery

UTF-16 Analyzer

Détecte les chaînes UTF-16 Little Endian dans un fichier binaire.

Ne produit aucun affichage.
Ajoute uniquement des Finding au Report.
"""

from __future__ import annotations

from ..binary_reader import BinaryReader
from ..models import (
    Finding,
    FindingType,
    Report,
    Severity,
)


class Utf16Analyzer:
    """
    Recherche les chaînes UTF-16LE contenant des caractères ASCII
    (octet haut égal à 0x00).
    """

    def __init__(self, minimum_length: int = 4):

        self.minimum_length = minimum_length

    # ---------------------------------------------------------

    @staticmethod
    def _is_utf16_char(low: int, high: int) -> bool:
        """
        Retourne True si les deux octets représentent un caractère
        ASCII imprimable encodé en UTF-16 Little Endian.

        Exemples :
            50 00 = 'P'
            72 00 = 'r'
            20 00 = ' '
        """

        return 32 <= low <= 126 and high == 0

    # ---------------------------------------------------------

    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:

        reader.seek(0)

        buffer = bytearray()
        start_offset = 0

        while reader.can_read(2):

            offset = reader.tell()

            low, high = reader.read(2)

            if self._is_utf16_char(low, high):

                if not buffer:
                    start_offset = offset

                buffer.extend((low, high))

            else:

                self._flush(
                    buffer,
                    start_offset,
                    report,
                )

                buffer.clear()

        #
        # Traite la dernière chaîne éventuelle
        #

        self._flush(
            buffer,
            start_offset,
            report,
        )

    # ---------------------------------------------------------

    def _flush(
        self,
        buffer: bytearray,
        offset: int,
        report: Report,
    ) -> None:

        if len(buffer) < self.minimum_length * 2:
            return

        try:

            text = buffer.decode(
                "utf-16le",
                errors="strict",
            )

        except UnicodeDecodeError:
            return

        #
        # Ignore les chaînes composées uniquement d'espaces
        #

        if not text.strip():
            return

        finding = Finding(
            offset=offset,
            length=len(buffer),
            category=FindingType.UTF16,
            description="UTF-16 string",
            value=text,
            severity=Severity.INFO,
        )

        report.add_finding(finding)

        #
        # Mise à jour des statistiques
        #

        if hasattr(report, "statistics"):
            report.statistics.utf16_strings += 1