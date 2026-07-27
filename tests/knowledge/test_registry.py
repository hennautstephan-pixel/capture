from __future__ import annotations

from capture_recovery.knowledge import DecoderRegistry
from capture_recovery.knowledge.decoder import Decoder


class DummyDecoder(Decoder):

    def can_decode(self, structure):
        return False

    def decode(self, structure):
        return None


def test_registry_empty():

    registry = DecoderRegistry()

    assert len(registry) == 0
    assert tuple(registry) == ()


def test_register():

    registry = DecoderRegistry()

    decoder = DummyDecoder()

    registry.register(decoder)

    assert len(registry) == 1
    assert registry.decoders == (decoder,)