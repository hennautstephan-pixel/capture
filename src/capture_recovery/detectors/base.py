from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import Detection


class Detector(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom du détecteur."""
        raise NotImplementedError

    @abstractmethod
    def detect(
        self,
        data: bytes,
    ) -> list[Detection]:
        """Analyse un buffer et retourne les détections."""
        raise NotImplementedError