"""
Abstract base class for all code generators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .context import GenerationContext
from .generated_file import GeneratedFile


class Generator(ABC):
    """
    Base class for every generator.

    Generators are pure components:
    - they never write files to disk;
    - they never modify global state;
    - they only generate GeneratedFile instances.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the unique generator name.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        definition: object,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:
        """
        Generate one or more files.

        Parameters
        ----------
        definition:
            Object describing what must be generated.

        context:
            Shared generation context.

        Returns
        -------
        tuple[GeneratedFile, ...]
            Generated files.
        """
        raise NotImplementedError