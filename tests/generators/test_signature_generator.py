from pathlib import Path

from capture_recovery.definitions.field_definition import FieldDefinition
from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.signature_generator import SignatureGenerator


def test_name():
    generator = SignatureGenerator()

    assert generator.name == "signature"


def test_generate_file():
    definition = ObjectDefinition(
        name="Fixture",
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    assert len(generated) == 1

    file = generated[0]

    assert file.name == "fixture_signature.py"


def test_generate_name_constant():
    definition = ObjectDefinition(
        name="Fixture",
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    source = generated[0].content

    assert 'NAME = "Fixture"' in source


def test_generate_field_count():
    definition = ObjectDefinition(
        name="Fixture",
        fields=(
            FieldDefinition("manufacturer", str),
            FieldDefinition("universe", int),
        ),
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    source = generated[0].content

    assert "FIELD_COUNT = 2" in source


def test_generate_field_names():
    definition = ObjectDefinition(
        name="Fixture",
        fields=(
            FieldDefinition("manufacturer", str),
            FieldDefinition("universe", int),
        ),
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    source = generated[0].content

    assert '"manufacturer"' in source
    assert '"universe"' in source


def test_generate_field_types():
    definition = ObjectDefinition(
        name="Fixture",
        fields=(
            FieldDefinition("manufacturer", str),
            FieldDefinition("universe", int),
        ),
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    source = generated[0].content

    assert "FIELD_TYPES" in source
    assert "str" in source
    assert "int" in source


def test_single_field_tuple():
    definition = ObjectDefinition(
        name="Fixture",
        fields=(
            FieldDefinition("manufacturer", str),
        ),
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = SignatureGenerator().generate(
        definition,
        context,
    )

    source = generated[0].content

    assert 'FIELD_NAMES = ("manufacturer",)' in source
    assert "FIELD_TYPES = (str,)" in source