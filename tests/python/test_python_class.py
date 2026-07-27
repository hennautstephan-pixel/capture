from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_field import PythonField


def test_defaults():
    cls = PythonClass("Fixture")

    assert cls.name == "Fixture"
    assert cls.docstring == ""
    assert cls.fields == ()
    assert cls.decorators == ()
    assert cls.bases == ()


def test_add_field():
    cls = PythonClass("Fixture")

    updated = cls.add_field(
        PythonField(
            name="manufacturer",
            annotation="str",
        )
    )

    assert cls.fields == ()
    assert updated.field_count == 1


def test_add_decorator():
    cls = PythonClass("Fixture")

    updated = cls.add_decorator("dataclass")

    assert updated.decorators == ("dataclass",)


def test_add_base():
    cls = PythonClass("Fixture")

    updated = cls.add_base("BaseFixture")

    assert updated.bases == ("BaseFixture",)


def test_multiple_fields():
    cls = (
        PythonClass("Fixture")
        .add_field(PythonField("manufacturer", "str"))
        .add_field(PythonField("model", "str"))
    )

    assert cls.field_count == 2


def test_has_docstring():
    cls = PythonClass(
        "Fixture",
        docstring="Fixture object",
    )

    assert cls.has_docstring


def test_is_immutable():
    cls = PythonClass("Fixture")

    updated = cls.add_decorator("dataclass")

    assert cls is not updated


def test_repr():
    cls = PythonClass("Fixture")

    assert "Fixture" in repr(cls)