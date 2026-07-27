from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from capture_recovery.structures import Structure

from .inference_result import InferenceResult


class InferenceRule(ABC):
    """
    Base class for every inference rule.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def match(
        self,
        structure: Structure,
    ) -> InferenceResult:
        """
        Try to recognize a structure.
        """