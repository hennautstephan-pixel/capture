from pathlib import Path

import pytest

from capture_recovery.generators.base import Generator
from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.generated_file import GeneratedFile


class DummyGenerator(Generator):

    @property
    def name(self) -> str:
        return "dummy"

    def generate(
        self,
        definition: object,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:
        return (
            GeneratedFile(
                path=Path("dummy.txt"),
                content="hello",
            ),
        )


def test_name():
    generator = DummyGenerator()

    assert generator.name == "dummy"


def test_generate_returns_tuple():
    generator = DummyGenerator()

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("generated"),
    )

    files = generator.generate(object(), context)

    assert isinstance(files, tuple)
    assert len(files) == 1
    assert files[0].name == "dummy.txt"


def test_generator_is_abstract():
    with pytest.raises(TypeError):
        Generator()