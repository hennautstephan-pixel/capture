from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .inference_context import InferenceContext
from .inference_result import InferenceResult


class InferenceRule(ABC):
    """
    Base class for every inference rule.

    Rules receive an InferenceContext instead of a raw Structure,
    allowing them to access knowledge, metadata, options and any
    future inference services through a single object.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Human-readable rule name.
        """
        ...

    @abstractmethod
    def match(
        self,
        context: InferenceContext,
    ) -> InferenceResult:
        """
        Try to recognize a structure from an inference context.
        """
        raise NotImplementedError