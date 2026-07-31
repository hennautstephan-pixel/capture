"""
Project reconstruction rules.

Defines how semantic recovery objects
are converted into Capture objects.
"""

from __future__ import annotations


class ReconstructionRules:
    """
    Rules used during project reconstruction.
    """

    FIXTURE_TYPES = {
        "fixture",
        "Fixture",
        "fixture_candidate",
    }

    STRUCTURE_TYPES = {
        "structure",
        "scene_structure",
        "Structure",
    }

    GROUP_TYPES = {
        "group",
        "Group",
    }

    BINDING_TYPES = {
        "binding",
        "structure_binding",
        "Binding",
    }

    PROJECT_TYPES = {
        "project",
        "Project",
    }

    def __init__(
        self,
        min_confidence: float = 0.5,
    ) -> None:
        self.min_confidence = min_confidence

    def confidence_ok(
        self,
        obj,
    ) -> bool:
        """Check confidence threshold."""
        return (
            self._get(obj, "confidence", 0.0)
            >= self.min_confidence
        )

    def is_project(self, obj) -> bool:
        return self._is_type(obj, self.PROJECT_TYPES)

    def is_structure(self, obj) -> bool:
        return self._is_type(obj, self.STRUCTURE_TYPES)

    def is_group(self, obj) -> bool:
        return self._is_type(obj, self.GROUP_TYPES)

    def is_binding(self, obj) -> bool:
        return self._is_type(obj, self.BINDING_TYPES)

    def is_fixture_candidate(
        self,
        obj,
    ) -> bool:
        return self._type(obj).lower() == "fixture_candidate"

    def is_fixture(
        self,
        obj,
    ) -> bool:
        object_type = self._type(obj).lower()

        if object_type == "fixture":
            return True

        if object_type != "fixture_candidate":
            return False

        confidence = self._get(obj, "confidence", 0.0)
        properties = self._properties(obj)

        evidence = properties.get("evidence", [])
        manufacturer = properties.get("manufacturer")
        model = properties.get("model")
        address = properties.get("address")
        universe = properties.get("universe")

        return (
            confidence >= 0.80
            or (manufacturer and model)
            or address is not None
            or universe is not None
            or len(evidence) >= 2
        )

    def _is_type(
        self,
        obj,
        valid_types,
    ) -> bool:
        return self._type(obj) in valid_types

    @staticmethod
    def _read(
        obj,
        key,
        default,
    ):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def _type(
        self,
        obj,
    ) -> str:
        return self._read(
            obj,
            "object_type",
            "",
        )

    def _get(
        self,
        obj,
        key,
        default=None,
    ):
        return self._read(
            obj,
            key,
            default,
        )

    def _properties(
        self,
        obj,
    ) -> dict:
        return self._read(
            obj,
            "properties",
            {},
        )