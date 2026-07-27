"""
Representation of a Python import statement.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True, order=True)
class PythonImport:
    """
    Immutable representation of a Python import.

    Examples
    --------
    import pathlib

    from dataclasses import dataclass

    from typing import Any, Iterable
    """

    module: str
    names: tuple[str, ...] = ()
    alias: str | None = None

    @property
    def is_from_import(self) -> bool:
        """
        Return True if this is a 'from ... import ...' statement.
        """
        return bool(self.names)

    @property
    def is_plain_import(self) -> bool:
        """
        Return True if this is an 'import ...' statement.
        """
        return not self.names

    def render(self) -> str:
        """
        Render the import statement.
        """
        if self.is_plain_import:
            if self.alias:
                return f"import {self.module} as {self.alias}"
            return f"import {self.module}"

        names = ", ".join(self.names)

        if self.alias:
            return (
                f"from {self.module} import {names} as {self.alias}"
            )

        return f"from {self.module} import {names}"