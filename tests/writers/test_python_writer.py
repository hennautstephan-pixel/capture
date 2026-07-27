from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_field import PythonField
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter


def test_empty_module():
    writer = PythonWriter()

    module = PythonModule("empty")

    assert writer.write(module) == ""


def test_simple_class():
    module = (
        PythonModule("fixture")
        .add_import(
            PythonImport(
                "dataclasses",
                ("dataclass",),
            )
        )
        .add_class(
            PythonClass(
                name="Fixture",
                decorators=("dataclass",),
                fields=(
                    PythonField(
                        "name",
                        "str",
                    ),
                ),
            )
        )
    )

    source = PythonWriter().write(module)

    assert (
        "from dataclasses import dataclass"
        in source
    )

    assert "@dataclass" in source

    assert "class Fixture:" in source

    assert "name: str" in source


def test_empty_class():
    module = PythonModule(
        "fixture"
    ).add_class(
        PythonClass(
            "Fixture",
        )
    )

    source = PythonWriter().write(module)

    assert "pass" in source