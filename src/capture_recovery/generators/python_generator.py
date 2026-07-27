"""
Base class for generators producing Python source files.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter

from .base import Generator
from .context import GenerationContext
from .generated_file import GeneratedFile


class PythonGenerator(Generator):
    """
    Base class for generators producing Python modules.
    """

    def build_file(
        self,
        module: PythonModule,
        filename: str,
        context: GenerationContext,
    ) -> GeneratedFile:
        """
        Render a Python module and wrap it in a GeneratedFile.
        """

        source = PythonWriter().write(module)

        return GeneratedFile(
            path=context.resolve(Path(filename)),
            content=source,
        )