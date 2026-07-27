from capture_recovery.knowledge.default_knowledge import (
    create_default_registry,
)


def test_default_decoder_registry():

    registry = create_default_registry()

    assert len(registry) == 3


def test_default_decoder_types():

    registry = create_default_registry()

    names = {
        decoder.object_type
        for decoder in registry
    }

    assert names == {
        "Fixture",
        "Universe",
        "Cue",
    }