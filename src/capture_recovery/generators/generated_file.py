"""
Representation of a file produced by a generator.

Generators never write directly to disk.
They only return instances of GeneratedFile.
A dedicated writer is responsible for persisting them.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class GeneratedFile:
    """
    Represents a generated source file.
    """

    path: Path
    content: str
    encoding: str = "utf-8"

    @property
    def suffix(self) -> str:
        return self.path.suffix

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def stem(self) -> str:
        return self.path.stem

    def with_content(self, content: str) -> "GeneratedFile":
        return GeneratedFile(
            path=self.path,
            content=content,
            encoding=self.encoding,
        )

    def __str__(self) -> str:
        return self.path.as_posix()