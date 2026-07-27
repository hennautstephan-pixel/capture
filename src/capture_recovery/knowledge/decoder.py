from __future__ import annotations

from abc import ABC, abstractmethod

from capture_recovery.structures.structure import Structure

from .semantic_object import SemanticObject


class Decoder(ABC):

    @abstractmethod
    def can_decode(
        self,
        structure: Structure,
    ) -> bool:
        ...

    @abstractmethod
    def decode(
        self,
        structure: Structure,
    ) -> SemanticObject | None:
        ...