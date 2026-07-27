"""
Capture Recovery

Structure Parser

Orchestre tous les analyseurs et produit un Report.
"""

from __future__ import annotations

from pathlib import Path

from .binary_reader import BinaryReader
from .models import Report

from .analyzers.ascii import AsciiAnalyzer
from .analyzers.utf16 import Utf16Analyzer
from .analyzers.entropy import EntropyAnalyzer
from .analyzers.pointers import PointerAnalyzer


class StructureParser:
    """
    Analyse complète d'un fichier Capture.
    """

    def __init__(self, filename: str | Path):

        self.filename = Path(filename)

        self.analyzers = [
            AsciiAnalyzer(),
            Utf16Analyzer(),
            EntropyAnalyzer(),
            PointerAnalyzer(),
        ]

    # ---------------------------------------------------------

    def run(self) -> Report:

        with BinaryReader(self.filename) as reader:

            report = Report(
                filename=str(self.filename),
                filesize=reader.size,
            )

            for analyzer in self.analyzers:

                analyzer.run(
                    reader,
                    report,
                )

            return report