from capture_recovery.formats import (
    CueBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)


def create_cue():

    return SemanticObject(
        object_type="Cue",
        identifier="Intro",
        properties={
            "cue_number": 1,
            "fade": 3.0,
            "delay": 0.5,
            "channels": {
                "1": 255,
                "2": 128,
            },
        },
    )


def test_build_cue():

    builder = CueBuilder()

    result = builder.build(
        create_cue(),
    )

    assert result.name == "Intro"

    assert result.number == 1


def test_build_preserves_properties():

    builder = CueBuilder()

    result = builder.build(
        create_cue(),
    )

    assert result.properties[
        "fade"
    ] == 3.0

    assert result.properties[
        "delay"
    ] == 0.5


def test_build_preserves_channels():

    builder = CueBuilder()

    result = builder.build(
        create_cue(),
    )

    assert result.properties[
        "channels"
    ] == {
        "1": 255,
        "2": 128,
    }


def test_can_build_cue():

    builder = CueBuilder()

    assert builder.can_build(
        create_cue(),
    ) is True


def test_cannot_build_fixture():

    builder = CueBuilder()

    fixture = SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={},
    )

    assert builder.can_build(
        fixture,
    ) is False


def test_build_default_number():

    builder = CueBuilder()

    cue = SemanticObject(
        object_type="Cue",
        identifier="Unknown",
        properties={},
    )

    result = builder.build(
        cue,
    )

    assert result.number == 0

    assert result.name == "Unknown"