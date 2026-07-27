from capture_recovery.definitions.object_definition import ObjectDefinition


def test_defaults():
    definition = ObjectDefinition(name="Fixture")

    assert definition.name == "Fixture"
    assert definition.description == ""
    assert definition.fields == ()
    assert definition.imports == ()
    assert definition.base_class is None
    assert definition.metadata == {}


def test_add_field():
    definition = ObjectDefinition(name="Fixture")

    updated = definition.add_field("manufacturer")

    assert definition.fields == ()
    assert updated.fields == ("manufacturer",)


def test_add_import():
    definition = ObjectDefinition(name="Fixture")

    updated = definition.add_import("pathlib.Path")

    assert definition.imports == ()
    assert updated.imports == ("pathlib.Path",)


def test_immutable():
    definition = ObjectDefinition(name="Fixture")

    updated = definition.add_field("name")

    assert definition is not updated


def test_multiple_fields():
    definition = (
        ObjectDefinition(name="Fixture")
        .add_field("manufacturer")
        .add_field("model")
    )

    assert definition.fields == (
        "manufacturer",
        "model",
    )


def test_multiple_imports():
    definition = (
        ObjectDefinition(name="Fixture")
        .add_import("pathlib.Path")
        .add_import("typing.Any")
    )

    assert definition.imports == (
        "pathlib.Path",
        "typing.Any",
    )