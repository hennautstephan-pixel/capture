from __future__ import annotations

from abc import ABC, abstractmethod

from capture_recovery.recovery import IntegrityReport


class BaseIntegrityCheck(ABC):

    @abstractmethod
    def check(
        self,
        project,
        report: IntegrityReport,
    ) -> None:
        """
        Analyse le projet et ajoute des problèmes dans report.
        """