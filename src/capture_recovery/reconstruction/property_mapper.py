"""
Property mapper.

Maps semantic object properties
to Capture fixture properties.
"""

from __future__ import annotations


class PropertyMapper:
    """
    Extract fixture properties.
    """

    def map(
        self,
        obj,
    ) -> dict:
        """
        Convert semantic properties
        into fixture data.
        """

        properties = obj.properties or {}

        return {

            "manufacturer": properties.get(
                "manufacturer",
            ),

            "model": properties.get(
                "model",
            ),

            "mode": properties.get(
                "mode",
            ),

            "universe": properties.get(
                "universe",
                0,
            ),

            "address": properties.get(
                "address",
                0,
            ),

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

            "focus_point": properties.get(
                "focus_point",
            ),

            "mount": properties.get(
                "mount",
            ),
        }