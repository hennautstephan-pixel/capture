from capture_recovery.generators.python_module_builder import PythonModuleBuilder


def test_create_empty_module():

    module = (
        PythonModuleBuilder("fixture")
        .build()
    )

    assert module.name == "fixture"


def test_add_import():

    module = (
        PythonModuleBuilder("fixture")
        .add_import(
            "dataclasses",
            ("dataclass",),
        )
        .build()
    )

    assert len(module.imports) == 1


def test_add_class():

    module = (
        PythonModuleBuilder("fixture")
        .begin_class("Fixture")
        .end_class()
        .build()
    )

    assert len(module.classes) == 1
    assert module.classes[0].name == "Fixture"


def test_add_field():

    module = (
        PythonModuleBuilder("fixture")
        .begin_class("Fixture")
        .add_field(
            "name",
            "str",
        )
        .end_class()
        .build()
    )

    cls = module.classes[0]

    assert len(cls.fields) == 1
    assert cls.fields[0].name == "name"
    assert cls.fields[0].annotation == "str"


def test_auto_close_class():

    module = (
        PythonModuleBuilder("fixture")
        .begin_class("Fixture")
        .build()
    )

    assert len(module.classes) == 1


def test_field_without_class():

    builder = PythonModuleBuilder("fixture")

    try:
        builder.add_field("name", "str")
        assert False
    except RuntimeError:
        pass