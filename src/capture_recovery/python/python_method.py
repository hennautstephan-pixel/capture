"""
Immutable representation of a Python method.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class PythonMethod:
    """
    Immutable representation of a Python method.
    """

    name: str
    parameters: tuple[str, ...] = field(default_factory=tuple)
    return_type: str = ""
    decorators: tuple[str, ...] = field(default_factory=tuple)
    body: tuple[str, ...] = field(default_factory=tuple)

    def add_parameter(
        self,
        parameter: str,
    ) -> "PythonMethod":
        return PythonMethod(
            name=self.name,
            parameters=(*self.parameters, parameter),
            return_type=self.return_type,
            decorators=self.decorators,
            body=self.body,
        )

    def add_decorator(
        self,
        decorator: str,
    ) -> "PythonMethod":
        return PythonMethod(
            name=self.name,
            parameters=self.parameters,
            return_type=self.return_type,
            decorators=(*self.decorators, decorator),
            body=self.body,
        )

    def add_line(
        self,
        line: str,
    ) -> "PythonMethod":
        return PythonMethod(
            name=self.name,
            parameters=self.parameters,
            return_type=self.return_type,
            decorators=self.decorators,
            body=(*self.body, line),
        )

    @property
    def parameter_count(self) -> int:
        return len(self.parameters)

    @property
    def decorator_count(self) -> int:
        return len(self.decorators)

    @property
    def line_count(self) -> int:
        return len(self.body)

    @property
    def has_return_type(self) -> bool:
        return bool(self.return_type)