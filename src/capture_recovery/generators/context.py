"""
Shared context used during code generation.

The generation context contains the global information required by
generators. It is immutable and shared by all generators during a
generation session.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class GenerationContext:
    """
    Shared generation context.

    Parameters
    ----------
    capture_version:
        Version of Capture for which the code is generated.

    output_directory:
        Root output directory.
    """

    capture_version: str
    output_directory: Path

    def resolve(self, relative_path: Path) -> Path:
        """
        Return the absolute path corresponding to a generated file.

        Parameters
        ----------
        relative_path:
            Relative path inside the output directory.

        Returns
        -------
        Path
            Absolute output path.
        """
        return self.output_directory / relative_path