from __future__ import annotations

from capture_recovery.inference import (
    InferenceContext,
    InferenceResult,
    InferenceRule,
)
from capture_recovery.models import DataType
from capture_recovery.structures import Structure


class Vector3Rule(InferenceRule):
    """
    Recognize a Vector3 structure.

    A Vector3 consists of three contiguous FLOAT32 values.
    """

    @property
    def name(self) -> str:
        return "Vector3"

    def match(
        self,
        context: InferenceContext | Structure,
    ) -> InferenceResult:

        # Compatibility during migration
        if isinstance(context, Structure):
            structure = context
        else:
            structure = context.structure

        if len(structure.fields) != 3:
            return InferenceResult(False)

        expected_offset = structure.offset

        for field in structure.fields:

            if field.datatype != DataType.FLOAT32:
                return InferenceResult(False)

            if field.offset != expected_offset:
                return InferenceResult(False)

            expected_offset += 4

        return InferenceResult(
            matched=True,
            structure_name="Vector3",
            confidence=0.95,
            reason="Three contiguous FLOAT32 values",
        )