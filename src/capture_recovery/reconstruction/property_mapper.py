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

    DEFAULT_VECTOR = (
        0.0,
        0.0,
        0.0,
    )

    DEFAULTS = {
        "manufacturer": None,
        "model": None,
        "mode": None,
        "universe": 0,
        "address": 0,
        "position": DEFAULT_VECTOR,
        "rotation": DEFAULT_VECTOR,
        "focus_point": None,
        "mount": None,
    }

    def map(self, obj) -> dict:
        """Convert semantic properties into fixture data."""

        properties = obj.properties or {}

        return {
            key: properties.get(key, default)
            for key, default in self.DEFAULTS.items()
        }
