from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_constant import PythonConstant
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter


def test_write_module_constants():
    module = (
        PythonModule("fixture")
        .add_constant(PythonConstant("NAME", '"Fixture"'))
        .add_constant(PythonConstant("FIELD_COUNT", "2"))
    )

    source = PythonWriter().write(module)

    assert 'NAME = "Fixture"' in source
    assert "FIELD_COUNT = 2" in source


def test_constants_before_classes():
    module = (
        PythonModule("fixture")
        .add_constant(PythonConstant("NAME", '"Fixture"'))
        .add_class(PythonClass("Fixture"))
    )

    source = PythonWriter().write(module)

    assert source.index('NAME = "Fixture"') < source.index("class Fixture")


def test_constants_after_imports():
    module = (
        PythonModule("fixture")
        .add_import(PythonImport("dataclasses", ("dataclass",)))
        .add_constant(PythonConstant("VERSION", '"2024"'))
    )

    source = PythonWriter().write(module)

    assert source.index("from dataclasses import dataclass") < source.index(
        'VERSION = "2024"'
    )


def test_constant_documentation():
    module = (
        PythonModule("fixture")
        .add_constant(
            PythonConstant(
                "NAME",
                '"Fixture"',
                documentation="Object name",
            )
        )
    )

    source = PythonWriter().write(module)

    assert "# Object name" in source
    assert 'NAME = "Fixture"' in source