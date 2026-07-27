"""
Representation of a Python class.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .python_field import PythonField
from .python_method import PythonMethod


@dataclass(slots=True, frozen=True)
class PythonClass:
    """
    Immutable representation of a Python class.
    """

    name: str
    decorators: tuple[str, ...] = field(default_factory=tuple)
    bases: tuple[str, ...] = field(default_factory=tuple)
    fields: tuple[PythonField, ...] = field(default_factory=tuple)
    methods: tuple[PythonMethod, ...] = field(default_factory=tuple)
    docstring: str = ""

    def add_decorator(
        self,
        decorator: str,
    ) -> "PythonClass":
        return PythonClass(
            name=self.name,
            decorators=(*self.decorators, decorator),
            bases=self.bases,
            fields=self.fields,
            methods=self.methods,
            docstring=self.docstring,
        )

    def add_base(
        self,
        base: str,
    ) -> "PythonClass":
        return PythonClass(
            name=self.name,
            decorators=self.decorators,
            bases=(*self.bases, base),
            fields=self.fields,
            methods=self.methods,
            docstring=self.docstring,
        )

    def add_field(
        self,
        field_: PythonField,
    ) -> "PythonClass":
        return PythonClass(
            name=self.name,
            decorators=self.decorators,
            bases=self.bases,
            fields=(*self.fields, field_),
            methods=self.methods,
            docstring=self.docstring,
        )

    def add_method(
        self,
        method: PythonMethod,
    ) -> "PythonClass":
        return PythonClass(
            name=self.name,
            decorators=self.decorators,
            bases=self.bases,
            fields=self.fields,
            methods=(*self.methods, method),
            docstring=self.docstring,
        )

    @property
    def has_docstring(self) -> bool:
        return bool(self.docstring)

    @property
    def decorator_count(self) -> int:
        return len(self.decorators)

    @property
    def base_count(self) -> int:
        return len(self.bases)

    @property
    def field_count(self) -> int:
        return len(self.fields)

    @property
    def method_count(self) -> int:
        return len(self.methods)