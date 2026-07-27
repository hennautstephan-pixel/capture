"""
Default Capture knowledge setup.
"""

from __future__ import annotations

from capture_recovery.decoders.cue_decoder import CueDecoder
from capture_recovery.decoders.fixture_decoder import FixtureDecoder
from capture_recovery.decoders.universe_decoder import UniverseDecoder
from capture_recovery.decoders.decoder_registry import DecoderRegistry
from capture_recovery.knowledge.signature_engine import SignatureEngine
from capture_recovery.knowledge.signature_registry import SignatureRegistry
from capture_recovery.knowledge.signatures.cue_signature import (
    CUE_SIGNATURE,
)
from capture_recovery.knowledge.signatures.fixture_signature import (
    FIXTURE_SIGNATURE,
)
from capture_recovery.knowledge.signatures.universe_signature import (
    UNIVERSE_SIGNATURE,
)


def create_default_registry() -> DecoderRegistry:
    """
    Create the standard Capture decoder registry.
    """

    signatures = SignatureRegistry()

    signatures.register(
        "Fixture",
        FIXTURE_SIGNATURE,
    )

    signatures.register(
        "Universe",
        UNIVERSE_SIGNATURE,
    )

    signatures.register(
        "Cue",
        CUE_SIGNATURE,
    )

    engine = SignatureEngine(
        signatures,
    )

    registry = DecoderRegistry()

    registry.register(
        FixtureDecoder(engine),
    )

    registry.register(
        UniverseDecoder(engine),
    )

    registry.register(
        CueDecoder(engine),
    )

    return registry