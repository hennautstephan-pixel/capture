from pathlib import Path

from capture_recovery.definitions.field_definition import FieldDefinition
from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.object_generator import ObjectGenerator


def make_context() -> GenerationContext:
    return GenerationContext(
        capture_version="2024",
        output_directory=Path("generated"),
    )


def test_generate_empty_object():

    definition = ObjectDefinition(
        name="Fixture",
    )

    files = ObjectGenerator().generate(
        definition,
        make_context(),
    )

    assert len(files) == 1

    generated = files[0]

    assert generated.name == "fixture.py"

    assert "@dataclass" in generated.content
    assert "class Fixture" in generated.content


def test_generate_fields():

    definition = ObjectDefinition(
        name="Fixture",
        fields=(
            FieldDefinition(
                name="manufacturer",
                python_type=str,
            ),
            FieldDefinition(
                name="universe",
                python_type=int,
            ),
        ),
    )

    files = ObjectGenerator().generate(
        definition,
        make_context(),
    )

    source = files[0].content

    assert "manufacturer: str" in source
    assert "universe: int" in source


def test_dataclass_decorator():

    definition = ObjectDefinition(
        name="Fixture",
    )

    files = ObjectGenerator().generate(
        definition,
        make_context(),
    )

    source = files[0].content

    assert "@dataclass" in source
    assert "slots=True" in source
    assert "frozen=True" in source