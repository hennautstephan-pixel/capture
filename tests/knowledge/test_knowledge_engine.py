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