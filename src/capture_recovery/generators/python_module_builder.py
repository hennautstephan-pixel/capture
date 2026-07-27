"""
Builder for PythonModule objects.
"""

from __future__ import annotations

from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_field import PythonField
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule


class PythonModuleBuilder:

    def __init__(self, module_name: str):

        self._module = PythonModule(name=module_name)
        self._current_class: PythonClass | None = None

    def add_import(
        self,
        module: str,
        names: tuple[str, ...],
    ) -> "PythonModuleBuilder":

        self._module = self._module.add_import(
            PythonImport(
                module=module,
                names=names,
            )
        )

        return self

    def begin_class(
        self,
        name: str,
        decorators: tuple[str, ...] = (),
    ) -> "PythonModuleBuilder":

        cls = PythonClass(name=name)

        for decorator in decorators:
            cls = cls.add_decorator(decorator)

        self._current_class = cls

        return self

    def add_field(
        self,
        name: str,
        annotation: str,
        default: str | None = None,
        documentation: str | None = None,
    ) -> "PythonModuleBuilder":

        if self._current_class is None:
            raise RuntimeError("No active class.")

        self._current_class = self._current_class.add_field(
            PythonField(
                name=name,
                annotation=annotation,
                default=default,
                documentation=documentation,
            )
        )

        return self

    def end_class(self) -> "PythonModuleBuilder":

        if self._current_class is None:
            raise RuntimeError("No active class.")

        self._module = self._module.add_class(
            self._current_class
        )

        self._current_class = None

        return self

    def build(self) -> PythonModule:

        if self._current_class is not None:
            self.end_class()

        return self._module