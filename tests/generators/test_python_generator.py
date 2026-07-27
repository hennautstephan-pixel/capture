from pathlib import Path

from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.python_generator import PythonGenerator
from capture_recovery.python.python_module import PythonModule


class DummyPythonGenerator(PythonGenerator):

    @property
    def name(self) -> str:
        return "dummy"

    def generate(self, definition, context):
        raise NotImplementedError


def test_build_file():
    generator = DummyPythonGenerator()

    module = PythonModule(
        name="fixture",
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = generator.build_file(
        module=module,
        filename="fixture.py",
        context=context,
    )

    assert generated.name == "fixture.py"
    assert generated.path == Path("/tmp") / "fixture.py"
    assert generated.content == ""


def test_build_file_with_content():
    generator = DummyPythonGenerator()

    module = (
        PythonModule(
            name="fixture",
        )
        .add_constant(
            __import__(
                "capture_recovery.python.python_constant",
                fromlist=["PythonConstant"],
            ).PythonConstant(
                "NAME",
                '"Fixture"',
            )
        )
    )

    context = GenerationContext(
        capture_version="2024",
        output_directory=Path("/tmp"),
    )

    generated = generator.build_file(
        module=module,
        filename="fixture.py",
        context=context,
    )

    assert 'NAME = "Fixture"' in generated.content