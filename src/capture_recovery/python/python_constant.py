"""
Representation of a Python module constant.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True, order=True)
class PythonConstant:
    """
    Immutable representation of a Python constant.
    """

    name: str
    value: str
    documentation: str = ""

    @property
    def has_documentation(self) -> bool:
        return bool(self.documentation)

    def render(self) -> str:
        """
        Render the constant.
        """

        return f"{self.name} = {self.value}"