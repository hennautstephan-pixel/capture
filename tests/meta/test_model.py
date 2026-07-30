from __future__ import annotations

from capture_recovery.meta.model import (
    Cardinality,
    FieldDefinition,
    ObjectDefinition,
)
from capture_recovery.models.data_type import DataType


def test_cardinality_values() -> None:
    assert Cardinality.REQUIRED.value == "required"
    assert Cardinality.OPTIONAL.value == "optional"
    assert Cardinality.REPEATED.value == "repeated"


def test_field_definition_defaults() -> None:
    field = FieldDefinition(
        name="label",
        datatype=DataType.STRING,
    )

    assert field.name == "label"
    assert field.datatype is DataType.STRING
    assert field.cardinality is Cardinality.OPTIONAL
    assert field.description == ""
    assert field.default is None
    assert field.confidence == 1.0
    assert field.aliases == ()
    assert field.metadata == {}


def test_field_definition_custom_values() -> None:
    field = FieldDefinition(
        name="channel",
        datatype=DataType.INT32,
        cardinality=Cardinality.REQUIRED,
        description="DMX channel",
        default=1,
        confidence=0.8,
        aliases=("address",),
        metadata={"unit": "dmx"},
    )

    assert field.default == 1
    assert field.aliases == ("address",)
    assert field.metadata["unit"] == "dmx"


def test_object_definition_defaults() -> None:
    obj = ObjectDefinition(name="Fixture")

    assert obj.name == "Fixture"
    assert obj.fields == ()
    assert obj.base_class == "SemanticObject"
    assert obj.generate_signature
    assert obj.generate_builder
    assert obj.generate_decoder
    assert obj.generate_tests
    assert obj.metadata == {}


def test_object_definition_with_fields() -> None:
    field = FieldDefinition(
        name="label",
        datatype=DataType.STRING,
    )

    obj = ObjectDefinition(
        name="Fixture",
        fields=(field,),
        metadata={"category": "lighting"},
    )

    assert obj.fields == (field,)
    assert obj.metadata["category"] == "lighting"
