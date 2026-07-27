"""
Capture Recovery

ASCII Analyzer

Détecte les chaînes ASCII imprimables dans un fichier binaire
et ajoute des objets Finding au Report.
"""

from __future__ import annotations

from ..binary_reader import BinaryReader
from ..models import (
    Finding,
    FindingType,
    Report,
    Severity,
)


class AsciiAnalyzer:
    """Analyseur de chaînes ASCII."""

    def __init__(
        self,
        minimum_length: int = 4,
        keep_duplicates: bool = False,
    ) -> None:

        self.minimum_length = minimum_length
        self.keep_duplicates = keep_duplicates

    @staticmethod
    def _is_printable(byte: int) -> bool:
        """Retourne True si l'octet est un caractère ASCII imprimable."""
        return 32 <= byte <= 126

    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:
        """
        Analyse le contenu du fichier et ajoute les chaînes ASCII
        trouvées au rapport.
        """

        reader.seek(0)

        buffer = bytearray()
        start_offset = 0
        seen: set[str] = set()

        while reader.can_read(1):

            offset = reader.tell()
            value = reader.read(1)[0]

            if self._is_printable(value):

                if not buffer:
                    start_offset = offset

                buffer.append(value)

            else:

                self._flush(
                    buffer,
                    start_offset,
                    report,
                    seen,
                )

                buffer.clear()

        # Dernière chaîne éventuelle
        self._flush(
            buffer,
            start_offset,
            report,
            seen,
        )

    def _flush(
        self,
        buffer: bytearray,
        offset: int,
        report: Report,
        seen: set[str],
    ) -> None:
        """
        Ajoute une chaîne ASCII au rapport si elle est valide.
        """

        if len(buffer) < self.minimum_length:
            return

        text = buffer.decode(
            "ascii",
            errors="ignore",
        )

        if not text.strip():
            return

        if not self.keep_duplicates:

            if text in seen:
                return

            seen.add(text)

        finding = Finding(
            offset=offset,
            length=len(buffer),
            category=FindingType.ASCII,
            description="ASCII string",
            value=text,
            severity=Severity.INFO,
        )

        report.add_finding(finding)