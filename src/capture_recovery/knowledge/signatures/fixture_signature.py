from __future__ import annotations

from capture_recovery.knowledge.field_signature import FieldSignature
from capture_recovery.knowledge.signature import Signature
from capture_recovery.models import DataType


FIXTURE_SIGNATURE = Signature(
    name="Fixture",
    required=(
        FieldSignature(
            name="name",
            datatype=DataType.STRING,
            weight=30,
            description="Fixture name",
        ),
        FieldSignature(
            name="universe",
            datatype=DataType.UINT16,
            weight=20,
            description="DMX universe",
        ),
        FieldSignature(
            name="address",
            datatype=DataType.UINT16,
            weight=20,
            description="DMX address",
        ),
    ),
    optional=(
        FieldSignature(
            name="fixture_id",
            datatype=DataType.UINT32,
            weight=10,
            description="Internal fixture identifier",
        ),
        FieldSignature(
            name="manufacturer",
            datatype=DataType.STRING,
            weight=10,
            description="Manufacturer",
        ),
        FieldSignature(
            name="model",
            datatype=DataType.STRING,
            weight=10,
            description="Fixture model",
        ),
        FieldSignature(
            name="mode",
            datatype=DataType.STRING,
            weight=10,
            description="DMX mode",
        ),
        FieldSignature(
            name="position",
            datatype=DataType.VECTOR3,
            weight=20,
            description="XYZ position",
        ),
        FieldSignature(
            name="rotation",
            datatype=DataType.VECTOR3,
            weight=10,
            description="Rotation",
        ),
        FieldSignature(
            name="scale",
            datatype=DataType.VECTOR3,
            weight=5,
            description="Scale",
        ),
        FieldSignature(
            name="color",
            datatype=DataType.COLOR_RGB,
            weight=5,
            description="RGB color",
        ),
        FieldSignature(
            name="dimmer",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Dimmer level",
        ),
        FieldSignature(
            name="pan",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Pan",
        ),
        FieldSignature(
            name="tilt",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Tilt",
        ),
        FieldSignature(
            name="zoom",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Zoom",
        ),
        FieldSignature(
            name="focus",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Focus",
        ),
        FieldSignature(
            name="iris",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Iris",
        ),
        FieldSignature(
            name="gobo",
            datatype=DataType.UINT16,
            weight=5,
            description="Gobo index",
        ),
        FieldSignature(
            name="frost",
            datatype=DataType.FLOAT32,
            weight=5,
            description="Frost",
        ),
        FieldSignature(
            name="enabled",
            datatype=DataType.BOOLEAN,
            weight=2,
            description="Enabled",
        ),
        FieldSignature(
            name="locked",
            datatype=DataType.BOOLEAN,
            weight=2,
            description="Locked",
        ),
        FieldSignature(
            name="visible",
            datatype=DataType.BOOLEAN,
            weight=2,
            description="Visible",
        ),
    ),
    minimum_score=70,
    description="Lighting fixture semantic signature",
)