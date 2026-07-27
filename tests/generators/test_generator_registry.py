from pathlib import Path

import pytest

from capture_recovery.generators.base import Generator
from capture_recovery.generators.context import GenerationContext
from capture_recovery.generators.generated_file import GeneratedFile
from capture_recovery.generators.registry import GeneratorRegistry


class DummyGenerator(Generator):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def generate(
        self,
        definition: object,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:
        return (
            GeneratedFile(
                path=Path("dummy.txt"),
                content="dummy",
            ),
        )


def test_register():
    registry = GeneratorRegistry()
    generator = DummyGenerator("dummy")

    registry.register(generator)

    assert len(registry) == 1
    assert "dummy" in registry


def test_duplicate_registration():
    registry = GeneratorRegistry()

    registry.register(DummyGenerator("dummy"))

    with pytest.raises(ValueError):
        registry.register(DummyGenerator("dummy"))


def test_get():
    registry = GeneratorRegistry()

    generator = DummyGenerator("dummy")
    registry.register(generator)

    assert registry.get("dummy") is generator


def test_unregister():
    registry = GeneratorRegistry()

    registry.register(DummyGenerator("dummy"))
    registry.unregister("dummy")

    assert len(registry) == 0


def test_generators():
    registry = GeneratorRegistry()

    a = DummyGenerator("a")
    b = DummyGenerator("b")

    registry.register(a)
    registry.register(b)

    assert registry.generators() == (a, b)


def test_names():
    registry = GeneratorRegistry()

    registry.register(DummyGenerator("a"))
    registry.register(DummyGenerator("b"))

    assert registry.names() == ("a", "b")


def test_clear():
    registry = GeneratorRegistry()

    registry.register(DummyGenerator("a"))
    registry.register(DummyGenerator("b"))

    registry.clear()

    assert len(registry) == 0


def test_iter():
    registry = GeneratorRegistry()

    a = DummyGenerator("a")
    b = DummyGenerator("b")

    registry.register(a)
    registry.register(b)

    assert tuple(registry) == (a, b)