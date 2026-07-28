"""
Structure binding model.

Defines the relation between a scene
structure and mounted fixtures.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StructureBinding:
    """
    Collection of fixtures attached
    to a structure.
    """

    structure_id: str

    fixtures: list[str] = field(
        default_factory=list,
    )

    properties: dict = field(
        default_factory=dict,
    )

    def add_fixture(
        self,
        fixture_name: str,
    ) -> None:
        """
        Add fixture reference.
        """

        if fixture_name not in self.fixtures:
            self.fixtures.append(
                fixture_name,
            )