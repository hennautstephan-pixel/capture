from __future__ import annotations

from capture_recovery.inference import (
    InferenceResult,
    InferenceRule,
)
from capture_recovery.models import DataType
from capture_recovery.structures import Structure


class Vector3Rule(InferenceRule):
    """
    Recognize a Vector3 structure.

    A Vector3 is defined as three consecutive FLOAT32 fields.
    """

    @property
    def name(self) -> str:
        return "Vector3"

    def match(
        self,
        structure: Structure,
    ) -> InferenceResult:

        if len(structure.fields) != 3:
            return InferenceResult(False)

        expected_offsets = [
            structure.offset,
            structure.offset + 4,
            structure.offset + 8,
        ]

        for field, expected in zip(
            structure.fields,
            expected_offsets,
        ):

            if field.datatype != DataType.FLOAT32:
                return InferenceResult(False)

            if field.offset != expected:
                return InferenceResult(False)

        return InferenceResult(
            matched=True,
            structure_name="Vector3",
            confidence=0.95,
            reason="Three contiguous FLOAT32 values",
        )