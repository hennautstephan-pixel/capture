"""
Fixture transform reconstruction.

Rebuilds fixture spatial data.
"""

from __future__ import annotations


class FixtureTransformReconstructor:
    """
    Reconstruct fixture position
    and rotation.
    """

    def reconstruct(
        self,
        obj,
    ) -> dict:
        """
        Extract transform data.
        """

        properties = obj.properties or {}

        return {

            "position": properties.get(
                "position",
                (
                    0.0,
                    0.0,
                    0.0,
                ),
            ),

            "rotation": properties.get(
                "rotation",
                (
                    0.0,
                    0.0,
                    0.0,
                ),
            ),

            "scale": properties.get(
                "scale",
                (
                    1.0,
                    1.0,
                    1.0,
                ),
            ),
        }