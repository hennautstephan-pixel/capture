from __future__ import annotations

from capture_recovery.knowledge import (
    DecoderRegistry,
    KnowledgeEngine,
    SemanticObject,
)

from capture_recovery.knowledge.decoder import Decoder

from capture_recovery.structures import Structure


class DummyDecoder(Decoder):

    def can_decode(self, structure):
        return True

    def decode(self, structure):

        return SemanticObject(
            object_type="Dummy",
            identifier=structure.offset,
        )


class RejectDecoder(Decoder):

    def can_decode(self, structure):
        return False

    def decode(self, structure):
        return None


def test_empty_engine():

    registry = DecoderRegistry()

    engine = KnowledgeEngine(registry)

    assert engine.infer([]) == ()


def test_no_decoder_accepts():

    registry = DecoderRegistry()

    registry.register(RejectDecoder())

    engine = KnowledgeEngine(registry)

    structure = Structure(
        name="A",
        offset=0,
        length=16,
    )

    assert engine.infer([structure]) == ()


def test_single_decoder():

    registry = DecoderRegistry()

    registry.register(DummyDecoder())

    engine = KnowledgeEngine(registry)

    structure = Structure(
        name="A",
        offset=10,
        length=32,
    )

    objects = engine.infer([structure])

    assert len(objects) == 1

    assert objects[0].object_type == "Dummy"

    assert objects[0].identifier == 10


def test_multiple_structures():

    registry = DecoderRegistry()

    registry.register(DummyDecoder())

    engine = KnowledgeEngine(registry)

    structures = (
        Structure(
            name="A",
            offset=1,
            length=10,
        ),
        Structure(
            name="B",
            offset=2,
            length=20,
        ),
    )

    objects = engine.infer(structures)

    assert len(objects) == 2

    assert objects[0].identifier == 1

    assert objects[1].identifier == 2

def test_analyze_empty():

    registry = DecoderRegistry()

    engine = KnowledgeEngine(registry)

    result = engine.analyze([])

    assert result.known_signature_count == 0
    assert result.unknown_signature_count == 0
    assert result.decoded_object_count == 0
    assert result.coverage == 0.0


def test_analyze_known_structure():

    registry = DecoderRegistry()

    registry.register(DummyDecoder())

    engine = KnowledgeEngine(registry)

    structure = Structure(
        name="Fixture",
        offset=100,
        length=32,
    )

    result = engine.analyze([structure])

    assert result.known_signature_count == 1
    assert result.unknown_signature_count == 0
    assert result.decoded_object_count == 1
    assert result.coverage == 1.0


def test_analyze_unknown_structure():

    registry = DecoderRegistry()

    registry.register(RejectDecoder())

    engine = KnowledgeEngine(registry)

    structure = Structure(
        name="Unknown",
        offset=10,
        length=16,
    )

    result = engine.analyze([structure])

    assert result.known_signature_count == 0
    assert result.unknown_signature_count == 1
    assert result.decoded_object_count == 0
    assert result.coverage == 0.0


def test_analyze_mixed():

    registry = DecoderRegistry()

    registry.register(DummyDecoder())
    registry.register(RejectDecoder())

    engine = KnowledgeEngine(registry)

    structures = (
        Structure(
            name="A",
            offset=1,
            length=16,
        ),
        Structure(
            name="B",
            offset=2,
            length=16,
        ),
    )

    result = engine.analyze(structures)

    assert result.known_signature_count == 2
    assert result.unknown_signature_count == 0
    assert result.decoded_object_count == 2
    assert len(result.decoded_objects) == 2


def test_infer_keeps_backward_compatibility():

    registry = DecoderRegistry()

    registry.register(DummyDecoder())

    engine = KnowledgeEngine(registry)

    structure = Structure(
        name="Fixture",
        offset=42,
        length=64,
    )

    objects = engine.infer([structure])

    assert isinstance(objects, tuple)
    assert len(objects) == 1
    assert objects[0].identifier == 42