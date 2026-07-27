from capture_recovery.builders.decoder_method_builder import DecoderMethodBuilder
from capture_recovery.definitions.field_definition import FieldDefinition
from capture_recovery.definitions.object_definition import ObjectDefinition


def test_empty_definition():
    definition = ObjectDefinition(
        name="Fixture",
    )

    method = DecoderMethodBuilder().build(definition)

    assert method.name == "decode"
    assert method.decorators == ("staticmethod",)
    assert method.parameters == ("reader: BinaryReader",)
    assert method.return_type == "Fixture"

    assert method.body == (
        "return Fixture(",
        ")",
    )


def test_string_field():
    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="manufacturer",
                python_type=str,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert (
        "    manufacturer=reader.read_string(),"
        in method.body
    )


def test_integer_field():
    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="universe",
                python_type=int,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert (
        "    universe=reader.read_uint32(),"
        in method.body
    )


def test_float_field():
    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="weight",
                python_type=float,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert (
        "    weight=reader.read_float(),"
        in method.body
    )


def test_bool_field():
    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="enabled",
                python_type=bool,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert (
        "    enabled=reader.read_bool(),"
        in method.body
    )


def test_unknown_type():
    class Vector3:
        pass

    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="position",
                python_type=Vector3,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert (
        "    position=reader.read_object(),"
        in method.body
    )


def test_multiple_fields():
    definition = (
        ObjectDefinition("Fixture")
        .add_field(
            FieldDefinition(
                name="manufacturer",
                python_type=str,
            )
        )
        .add_field(
            FieldDefinition(
                name="universe",
                python_type=int,
            )
        )
        .add_field(
            FieldDefinition(
                name="enabled",
                python_type=bool,
            )
        )
    )

    method = DecoderMethodBuilder().build(definition)

    assert method.body == (
        "return Fixture(",
        "    manufacturer=reader.read_string(),",
        "    universe=reader.read_uint32(),",
        "    enabled=reader.read_bool(),",
        ")",
    )