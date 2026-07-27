"""
Representation of a Python module.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .python_class import PythonClass
from .python_import import PythonImport


@dataclass(slots=True, frozen=True)
class PythonModule:
    """
    Immutable representation of a Python source module.
    """

    name: str
    docstring: str = ""
    imports: tuple[PythonImport, ...] = field(default_factory=tuple)
    classes: tuple[PythonClass, ...] = field(default_factory=tuple)

    def add_import(
        self,
        import_: PythonImport,
    ) -> "PythonModule":
        return PythonModule(
            name=self.name,
            docstring=self.docstring,
            imports=(*self.imports, import_),
            classes=self.classes,
        )

    def add_class(
        self,
        class_: PythonClass,
    ) -> "PythonModule":
        return PythonModule(
            name=self.name,
            docstring=self.docstring,
            imports=self.imports,
            classes=(*self.classes, class_),
        )

    @property
    def has_docstring(self) -> bool:
        return bool(self.docstring)

    @property
    def class_count(self) -> int:
        return len(self.classes)

    @property
    def import_count(self) -> int:
        return len(self.imports)