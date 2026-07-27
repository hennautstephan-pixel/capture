import pytest

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.decoder_registry import DecoderRegistry
from capture_recovery.knowledge.semantic_object import SemanticObject


class DummyObject(SemanticObject):
    pass


class DummyDecoder(Decoder):

    def can_decode(self, value) -> bool:
        return True

    def decode(self, reader):
        return DummyObject(
            object_type="Fixture",
            identifier="test",
        )


def test_empty_registry():
    registry = DecoderRegistry()

    assert len(registry) == 0
    assert registry.names == ()


def test_register_decoder():
    registry = DecoderRegistry()

    decoder = DummyDecoder()

    registry.register(
        "Fixture",
        decoder,
    )

    assert len(registry) == 1
    assert "Fixture" in registry


def test_decoder_for():
    registry = DecoderRegistry()

    decoder = DummyDecoder()

    registry.register(
        "Fixture",
        decoder,
    )

    assert registry.decoder_for("Fixture") is decoder


def test_missing_decoder():
    registry = DecoderRegistry()

    with pytest.raises(KeyError):
        registry.decoder_for("Unknown")


def test_decode():
    registry = DecoderRegistry()

    decoder = DummyDecoder()

    registry.register(
        "Fixture",
        decoder,
    )

    result = registry.decode(
        "Fixture",
        object(),
    )

    assert isinstance(
        result,
        DummyObject,
    )

    assert result.object_type == "Fixture"
    assert result.identifier == "test"


def test_iter_names():
    registry = DecoderRegistry()

    registry.register(
        "Fixture",
        DummyDecoder(),
    )

    registry.register(
        "Group",
        DummyDecoder(),
    )

    assert tuple(registry) == (
        "Fixture",
        "Group",
    )


def test_sorted_names():
    registry = DecoderRegistry()

    registry.register(
        "ZObject",
        DummyDecoder(),
    )

    registry.register(
        "AObject",
        DummyDecoder(),
    )

    assert registry.names == (
        "AObject",
        "ZObject",
    )