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