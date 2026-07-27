from pathlib import Path

from capture_recovery.definitions.field_definition import FieldDefinition
from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.decoder_generator import DecoderGenerator


def make_context() -> GenerationContext:
    return GenerationContext(
        capture_version="2024",
        output_directory=Path("generated"),
    )


def test_generate_empty_decoder():
    definition = ObjectDefinition(
        name="Fixture",
    )

    files = DecoderGenerator().generate(
        definition,
        make_context(),
    )

    assert len(files) == 1

    generated = files[0]

    assert generated.name == "fixture_decoder.py"

    assert "class FixtureDecoder:" in generated.content
    assert "@staticmethod" in generated.content
    assert "def decode(reader: BinaryReader) -> Fixture:" in generated.content


def test_generate_decoder_fields():
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
    )

    generated = DecoderGenerator().generate(
        definition,
        make_context(),
    )[0]

    source = generated.content

    assert "manufacturer=reader.read_string()" in source
    assert "universe=reader.read_uint32()" in source


def test_decoder_imports():
    definition = ObjectDefinition(
        name="Fixture",
    )

    generated = DecoderGenerator().generate(
        definition,
        make_context(),
    )[0]

    source = generated.content

    assert "BinaryReader" in source
    assert "from fixture import Fixture" in source


def test_decoder_filename():
    definition = ObjectDefinition(
        name="MyObject",
    )

    generated = DecoderGenerator().generate(
        definition,
        make_context(),
    )[0]

    assert generated.name == "myobject_decoder.py"