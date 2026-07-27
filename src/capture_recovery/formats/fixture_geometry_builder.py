"""
Fixture geometry builder.

Builds FixtureGeometry objects from recovered
semantic fixtures.
"""

from __future__ import annotations

from typing import Any

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .fixture_geometry import (
    FixtureGeometry,
)


class FixtureGeometryBuilder:
    """
    Convert semantic fixture geometry data into
    FixtureGeometry models.
    """

    def build(
        self,
        fixture: SemanticObject,
    ) -> FixtureGeometry:
        """
        Build geometry from a semantic fixture.
        """

        position = self._vector(
            fixture.get(
                "position",
            ),
            default=(
                0.0,
                0.0,
                0.0,
            ),
        )

        rotation = self._vector(
            fixture.get(
                "rotation",
            ),
            default=(
                0.0,
                0.0,
                0.0,
            ),
        )

        scale = self._vector(
            fixture.get(
                "scale",
            ),
            default=(
                1.0,
                1.0,
                1.0,
            ),
        )

        return FixtureGeometry(
            position=position,
            rotation=rotation,
            scale=scale,
            height=float(
                fixture.get(
                    "height",
                    0.0,
                )
            ),
            focus_point=fixture.get(
                "focus_point",
            ),
            metadata={
                "source": "SemanticObject",
                "identifier": fixture.identifier,
            },
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Return True for fixture objects.
        """

        return fixture.object_type == "Fixture"

    @staticmethod
    def _vector(
        value: Any,
        default: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        """
        Normalize vector values.
        """

        if value is None:
            return default

        if isinstance(value, tuple):
            if len(value) == 3:
                return (
                    float(value[0]),
                    float(value[1]),
                    float(value[2]),
                )

        if isinstance(value, list):
            if len(value) == 3:
                return (
                    float(value[0]),
                    float(value[1]),
                    float(value[2]),
                )

        return default

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )