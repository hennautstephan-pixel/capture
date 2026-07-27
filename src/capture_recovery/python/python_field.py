"""
Representation of a Python class field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class PythonField:
    """
    Immutable representation of a Python class field.
    """

    name: str
    annotation: str
    default: object | None = None
    documentation: str = ""

    @property
    def has_default(self) -> bool:
        """
        Return True if the field has a default value.
        """
        return self.default is not None

    def render(self) -> str:
        """
        Render the field declaration.
        """
        if self.has_default:
            return (
                f"{self.name}: {self.annotation} = "
                f"{self._format_default(self.default)}"
            )

        return f"{self.name}: {self.annotation}"

    @staticmethod
    def _format_default(value: Any) -> str:
        """
        Format a default value as valid Python code.
        """
        return repr(value)