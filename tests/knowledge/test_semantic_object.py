from __future__ import annotations

from capture_recovery.knowledge import SemanticObject


def test_creation():
    obj = SemanticObject(
        object_type="Fixture",
        identifier="PAR64",
    )

    assert obj.object_type == "Fixture"
    assert obj.identifier == "PAR64"
    assert obj.properties == {}
    assert obj.confidence == 1.0


def test_properties():
    obj = SemanticObject(
        object_type="Fixture",
        identifier="PAR64",
        properties={
            "address": 1,
            "universe": 2,
        },
    )

    assert obj.get("address") == 1
    assert obj.get("universe") == 2


def test_get_default():
    obj = SemanticObject(
        object_type="Fixture",
        identifier="PAR64",
    )

    assert obj.get("missing") is None
    assert obj.get("missing", 123) == 123


def test_has():
    obj = SemanticObject(
        object_type="Fixture",
        identifier="PAR64",
        properties={
            "address": 1,
        },
    )

    assert obj.has("address")
    assert not obj.has("rotation")


def test_key():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=42,
    )

    assert obj.key == ("Fixture", 42)


def test_property_count():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
        properties={
            "a": 1,
            "b": 2,
        },
    )

    assert obj.property_count == 2


def test_property_names():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
        properties={
            "z": 1,
            "a": 2,
        },
    )

    assert obj.property_names == (
        "a",
        "z",
    )


def test_contains():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
        properties={
            "color": "red",
        },
    )

    assert "color" in obj
    assert "mode" not in obj


def test_len():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
        properties={
            "a": 1,
            "b": 2,
            "c": 3,
        },
    )

    assert len(obj) == 3


def test_with_property():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
    )

    obj2 = obj.with_property("name", "Spot")

    assert obj.get("name") is None
    assert obj2.get("name") == "Spot"

    # L'objet original reste inchangé
    assert obj is not obj2


def test_with_confidence():
    obj = SemanticObject(
        object_type="Fixture",
        identifier=1,
    )

    obj2 = obj.with_confidence(0.75)

    assert obj.confidence == 1.0
    assert obj2.confidence == 0.75

    # L'objet original reste inchangé
    assert obj is not obj2