from __future__ import annotations

from capture_recovery.inference import (
    InferenceResult,
    InferenceRule,
)
from capture_recovery.models import DataType
from capture_recovery.structures import Structure


class ColorRGBARule(InferenceRule):
    """
    Recognize an RGBA color.

    Four contiguous FLOAT32 values
    whose values are inside [0,1].
    """

    @property
    def name(self) -> str:
        return "ColorRGBA"

    def match(
        self,
        structure: Structure,
    ) -> InferenceResult:

        if len(structure.fields) != 4:
            return InferenceResult(False)

        expected = structure.offset

        for field in structure.fields:

            if field.datatype != DataType.FLOAT32:
                return InferenceResult(False)

            if field.offset != expected:
                return InferenceResult(False)

            if not isinstance(field.value, (int, float)):
                return InferenceResult(False)

            if not 0.0 <= field.value <= 1.0:
                return InferenceResult(False)

            expected += 4

        return InferenceResult(
            matched=True,
            structure_name="ColorRGBA",
            confidence=0.98,
            reason="Four contiguous normalized FLOAT32 values",
        )