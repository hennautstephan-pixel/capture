"""
Shared context for a file scan.
"""

from dataclasses import dataclass

from ..binary_reader import BinaryReader
from .report import Report


@dataclass(slots=True)
class ScanContext:
    reader: BinaryReader
    report: Report