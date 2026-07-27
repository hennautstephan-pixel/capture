"""
Definition of a field belonging to an object.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class FieldDefinition:
    """
    Immutable description of an object field.
    """

    name: str
    python_type: type | Any
    default: object | None = None
    optional: bool = False
    documentation: str = ""

    @property
    def has_default(self) -> bool:
        """
        Return True if the field defines a default value.
        """
        return self.default is not None

    @property
    def type_name(self) -> str:
        """
        Return a human-readable type name.
        """
        try:
            return self.python_type.__name__
        except AttributeError:
            return str(self.python_type)