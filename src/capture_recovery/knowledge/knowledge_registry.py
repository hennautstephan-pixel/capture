"""
Global knowledge registry.

Aggregates named decoders and signatures.
"""

from __future__ import annotations

from .decoder import Decoder
from .decoder_registry import DecoderRegistry
from .signature import Signature
from .signature_registry import SignatureRegistry


class KnowledgeRegistry:
    """
    Central registry for knowledge components.

    Provides access to:
    - named decoders;
    - object signatures.
    """

    def __init__(self) -> None:
        self._decoders = DecoderRegistry()
        self._signatures = SignatureRegistry()

    def register_decoder(
        self,
        name: str,
        decoder: Decoder,
    ) -> None:
        """
        Register a decoder by object name.
        """

        self._decoders.register(
            name,
            decoder,
        )

    def register_signature(
        self,
        name: str,
        signature: Signature,
    ) -> None:
        """
        Register a signature by object name.
        """

        self._signatures.register(
            name,
            signature,
        )

    def decoder_for(
        self,
        name: str,
    ) -> Decoder:
        """
        Retrieve a decoder by object name.
        """

        return self._decoders.decoder_for(name)

    def signature_for(
        self,
        name: str,
    ) -> Signature:
        """
        Retrieve a signature by object name.
        """

        return self._signatures.signature_for(name)

    @property
    def decoders(self) -> DecoderRegistry:
        return self._decoders

    @property
    def signatures(self) -> SignatureRegistry:
        return self._signatures

    def __contains__(
        self,
        name: object,
    ) -> bool:
        return (
            name in self._decoders
            or name in self._signatures
        )