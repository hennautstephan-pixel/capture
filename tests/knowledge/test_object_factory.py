import pytest

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.knowledge_registry import KnowledgeRegistry
from capture_recovery.knowledge.object_factory import ObjectFactory
from capture_recovery.knowledge.signature import Signature
from capture_recovery.knowledge.semantic_object import SemanticObject


class DummyDecoder(Decoder):

    def can_decode(self, structure):
        return True

    def decode(self, structure):
        return SemanticObject(
            object_type="Fixture",
            identifier="decoded",
        )


def create_signature(name="Fixture"):
    return Signature(
        name=name,
        required=(),
        optional=(),
    )


def test_create_known_object():

    registry = KnowledgeRegistry()

    registry.register_signature(
        "Fixture",
        create_signature(),
    )

    factory = ObjectFactory(
        registry,
    )

    obj = factory.create(
        "Fixture",
        "fixture_001",
    )

    assert isinstance(
        obj,
        SemanticObject,
    )

    assert obj.object_type == "Fixture"
    assert obj.identifier == "fixture_001"


def test_create_unknown_object():

    registry = KnowledgeRegistry()

    factory = ObjectFactory(
        registry,
    )

    with pytest.raises(KeyError):
        factory.create(
            "Unknown",
            "001",
        )


def test_decode_known_object():

    registry = KnowledgeRegistry()

    decoder = DummyDecoder()

    registry.register_decoder(
        "Fixture",
        decoder,
    )

    factory = ObjectFactory(
        registry,
    )

    result = factory.decode(
        "Fixture",
        object(),
    )

    assert isinstance(
        result,
        SemanticObject,
    )

    assert result.object_type == "Fixture"
    assert result.identifier == "decoded"