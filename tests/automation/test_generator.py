from pathlib import Path

import pytest

from capture_recovery.automation.generator import (
    GenerationResult,
    Generator,
)


class DummyGenerator(Generator):

    name = "dummy"
    description = "Dummy generator"

    def generate(self, **kwargs):
        result = GenerationResult()
        result.add_file(Path("dummy.txt"))
        return result


def test_generation_result_empty():

    result = GenerationResult()

    assert result.file_count == 0
    assert result.generated_files == []
    assert result.warnings == []
    assert result.metadata == {}


def test_add_generated_file():

    result = GenerationResult()

    result.add_file(Path("hello.py"))

    assert result.file_count == 1
    assert result.generated_files == [Path("hello.py")]


def test_add_warning():

    result = GenerationResult()

    result.add_warning("warning")

    assert result.warnings == ["warning"]


def test_generator_identifier():

    generator = DummyGenerator()

    assert generator.identifier == "dummy"


def test_generator_generate():

    generator = DummyGenerator()

    result = generator.generate()

    assert result.file_count == 1
    assert result.generated_files[0].name == "dummy.txt"


def test_generator_is_abstract():

    with pytest.raises(TypeError):
        Generator()