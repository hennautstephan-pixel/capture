import pytest

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.knowledge_registry import KnowledgeRegistry
from capture_recovery.knowledge.signature import Signature
from capture_recovery.knowledge.semantic_object import SemanticObject


class DummyObject(SemanticObject):
    pass


class DummyDecoder(Decoder):

    def can_decode(self, structure):
        return False

    def decode(self, structure):
        return None


def create_signature(
    name="Fixture",
):
    return Signature(
        name=name,
        required=(),
        optional=(),
    )


def test_empty_registry():
    registry = KnowledgeRegistry()

    assert len(registry.decoders) == 0
    assert len(registry.signatures) == 0


def test_register_decoder():
    registry = KnowledgeRegistry()

    decoder = DummyDecoder()

    registry.register_decoder(
        "Fixture",
        decoder,
    )

    assert registry.decoder_for("Fixture") is decoder
    assert "Fixture" in registry.decoders


def test_register_signature():
    registry = KnowledgeRegistry()

    signature = create_signature()

    registry.register_signature(
        "Fixture",
        signature,
    )

    assert registry.signature_for("Fixture") is signature
    assert "Fixture" in registry.signatures


def test_missing_decoder():
    registry = KnowledgeRegistry()

    with pytest.raises(KeyError):
        registry.decoder_for("Unknown")


def test_missing_signature():
    registry = KnowledgeRegistry()

    with pytest.raises(KeyError):
        registry.signature_for("Unknown")


def test_contains_decoder():
    registry = KnowledgeRegistry()

    registry.register_decoder(
        "Fixture",
        DummyDecoder(),
    )

    assert "Fixture" in registry
    assert "Unknown" not in registry


def test_contains_signature():
    registry = KnowledgeRegistry()

    registry.register_signature(
        "Fixture",
        create_signature(),
    )

    assert "Fixture" in registry


def test_exposes_registries():
    registry = KnowledgeRegistry()

    assert registry.decoders is not None
    assert registry.signatures is not None


def test_shared_access():
    registry = KnowledgeRegistry()

    decoder = DummyDecoder()
    signature = create_signature()

    registry.register_decoder(
        "Fixture",
        decoder,
    )

    registry.register_signature(
        "Fixture",
        signature,
    )

    assert registry.decoder_for("Fixture") is decoder
    assert registry.signature_for("Fixture") is signature