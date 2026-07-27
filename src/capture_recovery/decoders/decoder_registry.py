"""
Semantic decoder registry.
"""

from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.knowledge.decoder import Decoder


class DecoderRegistry:
    """
    Registry containing semantic decoders.
    """

    def __init__(self) -> None:
        self._decoders: list[Decoder] = []

    def register(
        self,
        decoder: Decoder,
    ) -> None:
        self._decoders.append(
            decoder,
        )

    def register_many(
        self,
        decoders: Iterable[Decoder],
    ) -> None:
        for decoder in decoders:
            self.register(
                decoder,
            )

    @property
    def decoders(self) -> tuple[Decoder, ...]:
        return tuple(
            self._decoders
        )

    def __iter__(self):
        return iter(
            self._decoders
        )

    def __len__(self) -> int:
        return len(
            self._decoders
        )