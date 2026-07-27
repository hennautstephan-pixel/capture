"""
Utility class used to generate formatted source code.
"""

from __future__ import annotations


class CodeWriter:
    """
    Helper used to build source code with proper indentation.
    """

    INDENT = "    "

    def __init__(self) -> None:
        self._lines: list[str] = []
        self._indent = 0

    @property
    def indentation(self) -> int:
        """
        Current indentation level.
        """
        return self._indent

    def line(self, text: str = "") -> None:
        """
        Append one line.
        """
        if text:
            self._lines.append(f"{self.INDENT * self._indent}{text}")
        else:
            self._lines.append("")

    def blank(self) -> None:
        """
        Append an empty line.
        """
        self.line()

    def indent(self) -> None:
        """
        Increase indentation.
        """
        self._indent += 1

    def dedent(self) -> None:
        """
        Decrease indentation.
        """
        if self._indent == 0:
            raise ValueError("Indentation level cannot become negative.")

        self._indent -= 1

    def extend(self, lines: list[str] | tuple[str, ...]) -> None:
        """
        Append multiple lines.
        """
        for line in lines:
            self.line(line)

    def render(self) -> str:
        """
        Return the generated source code.
        """
        return "\n".join(self._lines) + "\n"

    def clear(self) -> None:
        """
        Remove every generated line.
        """
        self._lines.clear()
        self._indent = 0