from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_method import PythonMethod
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter


def test_write_empty_method():
    module = (
        PythonModule("fixture")
        .add_class(
            PythonClass("Fixture").add_method(
                PythonMethod("decode")
            )
        )
    )

    source = PythonWriter().write(module)

    assert "def decode():" in source
    assert "pass" in source


def test_write_staticmethod():
    module = (
        PythonModule("fixture")
        .add_class(
            PythonClass("Fixture").add_method(
                PythonMethod("decode")
                .add_decorator("staticmethod")
                .add_parameter("reader: BinaryReader")
                .add_line("return None")
            )
        )
    )

    source = PythonWriter().write(module)

    assert "@staticmethod" in source
    assert "def decode(reader: BinaryReader):" in source
    assert "return None" in source


def test_write_return_type():
    module = (
        PythonModule("fixture")
        .add_class(
            PythonClass("Fixture").add_method(
                PythonMethod(
                    name="decode",
                    return_type="Fixture",
                )
                .add_parameter("reader: BinaryReader")
                .add_line("return Fixture()")
            )
        )
    )

    source = PythonWriter().write(module)

    assert "def decode(reader: BinaryReader) -> Fixture:" in source


def test_fields_then_methods():
    from capture_recovery.python.python_field import PythonField

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
                "Fixture",
                decorators=("dataclass",),
            )
            .add_field(
                PythonField(
                    "name",
                    "str",
                )
            )
            .add_method(
                PythonMethod("reset")
                .add_line("pass")
            )
        )
    )

    source = PythonWriter().write(module)

    assert "name: str" in source
    assert "def reset():" in source