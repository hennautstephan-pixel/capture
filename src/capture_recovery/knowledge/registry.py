"""
Global knowledge registry.
"""

from __future__ import annotations

from .decoder_registry import DecoderRegistry
from .signature_registry import SignatureRegistry


class KnowledgeRegistry:
    """
    Central registry for decoders and signatures.
    """

    def __init__(self) -> None:
        self.decoders = DecoderRegistry()
        self.signatures = SignatureRegistry()

    def register_decoder(
        self,
        name: str,
        decoder,
    ) -> None:
        self.decoders.register(
            name,
            decoder,
        )

    def register_signature(
        self,
        name: str,
        signature,
    ) -> None:
        self.signatures.register(
            name,
            signature,
        )

    def decoder_for(
        self,
        name: str,
    ):
        return self.decoders.decoder_for(name)

    def signature_for(
        self,
        name: str,
    ):
        return self.signatures.signature_for(name)