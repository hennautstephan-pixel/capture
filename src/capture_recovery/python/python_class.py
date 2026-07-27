"""
Representation of a Python class.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .python_field import PythonField


@dataclass(slots=True, frozen=True)
class PythonClass:
    """
    Immutable representation of a Python class.
    """

    name: str
    docstring: str = ""
    decorators: tuple[str, ...] = field(default_factory=tuple)
    bases: tuple[str, ...] = field(default_factory=tuple)
    fields: tuple[PythonField, ...] = field(default_factory=tuple)

    def add_field(
        self,
        field_: PythonField,
    ) -> "PythonClass":
        """
        Return a copy with an additional field.
        """
        return PythonClass(
            name=self.name,
            docstring=self.docstring,
            decorators=self.decorators,
            bases=self.bases,
            fields=(*self.fields, field_),
        )

    def add_decorator(
        self,
        decorator: str,
    ) -> "PythonClass":
        """
        Return a copy with an additional decorator.
        """
        return PythonClass(
            name=self.name,
            docstring=self.docstring,
            decorators=(*self.decorators, decorator),
            bases=self.bases,
            fields=self.fields,
        )

    def add_base(
        self,
        base: str,
    ) -> "PythonClass":
        """
        Return a copy with an additional base class.
        """
        return PythonClass(
            name=self.name,
            docstring=self.docstring,
            decorators=self.decorators,
            bases=(*self.bases, base),
            fields=self.fields,
        )

    @property
    def field_count(self) -> int:
        """
        Return the number of fields.
        """
        return len(self.fields)

    @property
    def has_docstring(self) -> bool:
        """
        Return True if the class has a docstring.
        """
        return bool(self.docstring)