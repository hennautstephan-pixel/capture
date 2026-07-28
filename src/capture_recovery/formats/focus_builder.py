"""
Focus point builder.

Builds fixture focus targets from
semantic fixture objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .focus_point import (
    FocusPoint,
)


class FocusBuilder:
    """
    Build fixture focus points.
    """

    def build(
        self,
        fixture: SemanticObject,
    ) -> FocusPoint:
        """
        Convert focus data into
        FocusPoint.
        """

        focus = fixture.properties.get(
            "focus_point",
            {},
        )

        if isinstance(
            focus,
            tuple,
        ):

            focus = {
                "x": focus[0],
                "y": focus[1],
                "z": focus[2],
            }

        if isinstance(
            focus,
            dict,
        ):

            return FocusPoint(
                x=focus.get(
                    "x",
                    0.0,
                ),

                y=focus.get(
                    "y",
                    0.0,
                ),

                z=focus.get(
                    "z",
                    0.0,
                ),

                properties=fixture.properties.copy(),
            )

        # Legacy named focus point:
        # "Centre plateau", "Face", etc.
        return FocusPoint(
            x=0.0,

            y=0.0,

            z=0.0,

            properties={
                **fixture.properties,

                "focus_name": focus,
            },
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:
        """
        Check fixture type.
        """

        return (
            fixture.object_type
            == "Fixture"
        )