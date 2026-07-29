"""
Base classes for the automation framework.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class GenerationResult:
    """
    Result returned by a generator.
    """

    generated_files: list[Path] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def file_count(self) -> int:
        return len(self.generated_files)

    def add_file(self, path: Path) -> None:
        self.generated_files.append(path)

    def add_warning(self, message: str) -> None:
        self.warnings.append(message)


class Generator(ABC):
    """
    Base class for every automation generator.
    """

    name: str = ""
    description: str = ""

    @abstractmethod
    def generate(self, **kwargs: Any) -> GenerationResult:
        """
        Generate one or more files.

        Returns
        -------
        GenerationResult
            Description of everything generated.
        """
        raise NotImplementedError

    @property
    def identifier(self) -> str:
        """
        Unique identifier used by the registry.
        """
        return self.name.lower()