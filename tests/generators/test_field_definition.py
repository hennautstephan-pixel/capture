from typing import Any

from capture_recovery.definitions.field_definition import FieldDefinition


def test_defaults():
    field = FieldDefinition(
        name="manufacturer",
        python_type=str,
    )

    assert field.name == "manufacturer"
    assert field.python_type is str
    assert field.default is None
    assert field.optional is False
    assert field.documentation == ""


def test_has_default_false():
    field = FieldDefinition(
        name="manufacturer",
        python_type=str,
    )

    assert field.has_default is False


def test_has_default_true():
    field = FieldDefinition(
        name="universe",
        python_type=int,
        default=1,
    )

    assert field.has_default is True


def test_type_name_builtin():
    field = FieldDefinition(
        name="enabled",
        python_type=bool,
    )

    assert field.type_name == "bool"


def test_type_name_typing():
    field = FieldDefinition(
        name="value",
        python_type=Any,
    )

    assert "Any" in field.type_name


def test_optional():
    field = FieldDefinition(
        name="description",
        python_type=str,
        optional=True,
    )

    assert field.optional is True