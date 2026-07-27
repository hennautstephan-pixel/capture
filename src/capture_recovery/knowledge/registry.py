"""
Decoder registry used by KnowledgeEngine.
"""

from __future__ import annotations

from .decoder import Decoder


class DecoderRegistry:
    """
    Registry containing decoders used for inference.

    Decoders are tested sequentially against structures.
    """

    def __init__(self) -> None:
        self._decoders: list[Decoder] = []

    def register(
        self,
        decoder: Decoder,
    ) -> None:
        """
        Register a decoder.
        """

        self._decoders.append(decoder)

    @property
    def decoders(self) -> tuple[Decoder, ...]:
        """
        Return all registered decoders.
        """

        return tuple(self._decoders)

    def __len__(self) -> int:
        return len(self._decoders)

    def __iter__(self):
        return iter(self._decoders)