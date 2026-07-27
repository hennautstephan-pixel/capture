from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule


def test_defaults():
    module = PythonModule("fixtures")

    assert module.name == "fixtures"
    assert module.imports == ()
    assert module.classes == ()
    assert module.docstring == ""
    assert module.import_count == 0
    assert module.class_count == 0


def test_add_import():
    module = PythonModule("fixtures")

    updated = module.add_import(
        PythonImport("dataclasses")
    )

    assert module.import_count == 0
    assert module.imports == ()

    assert updated.import_count == 1
    assert updated.imports == (
        PythonImport("dataclasses"),
    )


def test_add_class():
    module = PythonModule("fixtures")

    updated = module.add_class(
        PythonClass("Fixture")
    )

    assert module.class_count == 0
    assert module.classes == ()

    assert updated.class_count == 1
    assert updated.classes[0].name == "Fixture"


def test_has_docstring():
    module = PythonModule(
        "fixtures",
        docstring="Fixture models",
    )

    assert module.has_docstring


def test_is_immutable():
    module = PythonModule("fixtures")

    updated = module.add_import(
        PythonImport("typing")
    )

    assert module is not updated
    assert module.imports == ()
    assert updated.import_count == 1


def test_repr():
    module = PythonModule("fixtures")

    assert "fixtures" in repr(module)


def test_multiple_imports():
    module = (
        PythonModule("fixtures")
        .add_import(PythonImport("typing"))
        .add_import(PythonImport("dataclasses"))
    )

    assert module.import_count == 2
    assert module.imports == (
        PythonImport("typing"),
        PythonImport("dataclasses"),
    )


def test_multiple_classes():
    module = (
        PythonModule("fixtures")
        .add_class(PythonClass("Fixture"))
        .add_class(PythonClass("Universe"))
    )

    assert module.class_count == 2
    assert module.classes[0].name == "Fixture"
    assert module.classes[1].name == "Universe"