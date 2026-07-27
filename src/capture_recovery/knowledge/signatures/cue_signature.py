from __future__ import annotations

from capture_recovery.knowledge.field_signature import FieldSignature
from capture_recovery.knowledge.signature import Signature
from capture_recovery.models import DataType


CUE_SIGNATURE = Signature(
    name="Cue",
    required=(
        FieldSignature(
            name="name",
            datatype=DataType.STRING,
            weight=40,
            description="Cue name",
        ),
        FieldSignature(
            name="cue_number",
            datatype=DataType.UINT16,
            weight=30,
            description="Cue number",
        ),
    ),
    optional=(
        FieldSignature(
            name="fade_in",
            datatype=DataType.FLOAT32,
            weight=10,
            description="Fade in time",
        ),
        FieldSignature(
            name="fade_out",
            datatype=DataType.FLOAT32,
            weight=10,
            description="Fade out time",
        ),
        FieldSignature(
            name="delay",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Cue delay",
        ),
        FieldSignature(
            name="enabled",
            datatype=DataType.BOOLEAN,
            weight=5,
            description="Cue enabled",
        ),
    ),
    minimum_score=70,
    description="Lighting cue semantic signature",
)