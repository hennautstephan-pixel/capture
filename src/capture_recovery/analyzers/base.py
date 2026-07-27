"""
Common interfaces for analyzers.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from ..binary_reader import BinaryReader
from ..models import Report


class Analyzer(ABC):
    """
    Base class implemented by every analyzer.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human readable analyzer name.
        """

    @abstractmethod
    def run(
        self,
        reader: BinaryReader,
        report: Report,
    ) -> None:
        """
        Analyze the binary file.
        """

    def __str__(self):

        return self.name