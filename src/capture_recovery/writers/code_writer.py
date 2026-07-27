"""
Utilities for writing indented source code.
"""

from __future__ import annotations


class CodeWriter:
    """
    Helper for generating indented source code.
    """

    INDENT = "    "

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._level = 0

    @property
    def indentation(self) -> int:
        return self._level

    def indent(self) -> None:
        self._level += 1

    def dedent(self) -> None:
        if self._level == 0:
            raise ValueError("Cannot dedent below zero.")
        self._level -= 1

    def line(self, text: str = "") -> None:
        if text:
            self._lines.append(f"{self.INDENT * self._level}{text}")
        else:
            self._lines.append("")

    def blank(self) -> None:
        self._lines.append("")

    def extend(self, lines: list[str]) -> None:
        for line in lines:
            self.line(line)

    def clear(self) -> None:
        self._lines.clear()
        self._level = 0

    def render(self) -> str:
        if not self._lines:
            return ""
        return "\n".join(self._lines) + "\n"