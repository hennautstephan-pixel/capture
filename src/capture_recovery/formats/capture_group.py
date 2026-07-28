"""
Capture fixture groups.

Contains models for grouping fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CaptureGroup:
    """
    Fixture group model.

    Represents a named collection of fixtures.
    """

    name: str

    fixtures: list[str] = field(
        default_factory=list,
    )

    properties: dict = field(
        default_factory=dict,
    )

    def add_fixture(
        self,
        fixture: str,
    ) -> None:
        """
        Add a fixture reference.
        """

        self.fixtures.append(
            fixture,
        )

    def __len__(self) -> int:
        return len(
            self.fixtures,
        )