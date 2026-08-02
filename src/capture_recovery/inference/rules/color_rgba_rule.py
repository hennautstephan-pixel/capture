from __future__ import annotations

from capture_recovery.inference import (
    InferenceContext,
    InferenceResult,
    InferenceRule,
)
from capture_recovery.models import DataType
from capture_recovery.structures import Structure


class ColorRGBARule(InferenceRule):
    """
    Recognize an RGBA color.

    An RGBA color consists of four contiguous FLOAT32 values
    normalized in the range [0.0, 1.0].
    """

    @property
    def name(self) -> str:
        return "ColorRGBA"

    def match(
        self,
        context: InferenceContext | Structure,
    ) -> InferenceResult:

        # Compatibility during migration
        if isinstance(context, Structure):
            structure = context
        else:
            structure = context.structure

        if len(structure.fields) != 4:
            return InferenceResult(False)

        expected_offset = structure.offset

        for field in structure.fields:

            if field.datatype != DataType.FLOAT32:
                return InferenceResult(False)

            if field.offset != expected_offset:
                return InferenceResult(False)

            if not isinstance(field.value, (int, float)):
                return InferenceResult(False)

            if not 0.0 <= field.value <= 1.0:
                return InferenceResult(False)

            expected_offset += 4

        return InferenceResult(
            matched=True,
            structure_name="ColorRGBA",
            confidence=0.98,
            reason="Four contiguous normalized FLOAT32 values",
        )