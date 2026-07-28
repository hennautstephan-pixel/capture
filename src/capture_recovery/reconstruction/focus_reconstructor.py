"""
Focus reconstruction.

Rebuilds fixture focus information.
"""

from __future__ import annotations


class FocusReconstructor:
    """
    Reconstruct focus points.
    """

    def reconstruct(
        self,
        obj,
    ) -> dict:
        """
        Extract focus information.
        """

        properties = obj.properties or {}

        return {

            "focus_point": properties.get(
                "focus_point",
            ),

            "pan": properties.get(
                "pan",
                0.0,
            ),

            "tilt": properties.get(
                "tilt",
                0.0,
            ),
        }