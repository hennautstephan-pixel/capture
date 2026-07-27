from __future__ import annotations

from capture_recovery.knowledge.field_signature import FieldSignature
from capture_recovery.knowledge.signature import Signature
from capture_recovery.models import DataType


UNIVERSE_SIGNATURE = Signature(
    name="Universe",
    required=(
        FieldSignature(
            name="name",
            datatype=DataType.STRING,
            weight=30,
            description="Universe name",
        ),
        FieldSignature(
            name="universe",
            datatype=DataType.UINT16,
            weight=30,
            description="Universe number",
        ),
    ),
    optional=(
        FieldSignature(
            name="protocol",
            datatype=DataType.STRING,
            weight=10,
            description="Output protocol",
        ),
        FieldSignature(
            name="subnet",
            datatype=DataType.UINT16,
            weight=10,
            description="Subnet number",
        ),
        FieldSignature(
            name="net",
            datatype=DataType.UINT16,
            weight=10,
            description="Art-Net net",
        ),
        FieldSignature(
            name="priority",
            datatype=DataType.UINT8,
            weight=5,
            description="sACN priority",
        ),
        FieldSignature(
            name="enabled",
            datatype=DataType.BOOLEAN,
            weight=5,
            description="Universe enabled",
        ),
        FieldSignature(
            name="ip_address",
            datatype=DataType.STRING,
            weight=10,
            description="Destination IP address",
        ),
        FieldSignature(
            name="port",
            datatype=DataType.UINT16,
            weight=5,
            description="UDP port",
        ),
    ),
    minimum_score=60,
    description="Lighting universe semantic signature",
)