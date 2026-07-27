from __future__ import annotations

from capture_recovery.knowledge.signatures.fixture_signature import (
    FIXTURE_SIGNATURE,
)
from capture_recovery.models import DataType


def test_name() -> None:
    assert FIXTURE_SIGNATURE.name == "Fixture"


def test_description() -> None:
    assert FIXTURE_SIGNATURE.description == (
        "Lighting fixture semantic signature"
    )


def test_minimum_score() -> None:
    assert FIXTURE_SIGNATURE.minimum_score == 70


def test_required_fields() -> None:
    assert len(FIXTURE_SIGNATURE.required) == 3

    names = tuple(field.name for field in FIXTURE_SIGNATURE.required)

    assert names == (
        "name",
        "universe",
        "address",
    )


def test_required_datatypes() -> None:
    fields = {
        field.name: field
        for field in FIXTURE_SIGNATURE.required
    }

    assert fields["name"].datatype is DataType.STRING
    assert fields["universe"].datatype is DataType.UINT16
    assert fields["address"].datatype is DataType.UINT16


def test_optional_contains_position() -> None:
    assert FIXTURE_SIGNATURE.contains("position")

    field = FIXTURE_SIGNATURE.field("position")

    assert field is not None
    assert field.datatype is DataType.VECTOR3


def test_optional_contains_rotation() -> None:
    field = FIXTURE_SIGNATURE.field("rotation")

    assert field is not None
    assert field.datatype is DataType.VECTOR3


def test_optional_contains_color() -> None:
    field = FIXTURE_SIGNATURE.field("color")

    assert field is not None
    assert field.datatype is DataType.COLOR_RGB


def test_optional_contains_boolean_fields() -> None:
    for name in (
        "enabled",
        "locked",
        "visible",
    ):
        field = FIXTURE_SIGNATURE.field(name)

        assert field is not None
        assert field.datatype is DataType.BOOLEAN


def test_maximum_score() -> None:
    expected = sum(
        field.weight
        for field in FIXTURE_SIGNATURE.fields
    )

    assert FIXTURE_SIGNATURE.maximum_score == expected


def test_iteration() -> None:
    fields = list(FIXTURE_SIGNATURE)

    assert len(fields) == len(FIXTURE_SIGNATURE)


def test_contains_operator() -> None:
    assert "name" in FIXTURE_SIGNATURE
    assert "manufacturer" in FIXTURE_SIGNATURE
    assert "foobar" not in FIXTURE_SIGNATURE


def test_field_lookup() -> None:
    field = FIXTURE_SIGNATURE.field("manufacturer")

    assert field is not None
    assert field.name == "manufacturer"


def test_missing_field() -> None:
    assert FIXTURE_SIGNATURE.field("does_not_exist") is None


def test_required_names() -> None:
    assert FIXTURE_SIGNATURE.required_names() == (
        "name",
        "universe",
        "address",
    )


def test_optional_names() -> None:
    names = FIXTURE_SIGNATURE.optional_names()

    assert "manufacturer" in names
    assert "model" in names
    assert "position" in names
    assert "rotation" in names