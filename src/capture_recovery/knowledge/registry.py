from __future__ import annotations

from .decoder import Decoder


class DecoderRegistry:

    def __init__(self) -> None:
        self._decoders: list[Decoder] = []

    def register(
        self,
        decoder: Decoder,
    ) -> None:
        self._decoders.append(decoder)

    @property
    def decoders(self) -> tuple[Decoder, ...]:
        return tuple(self._decoders)

    def __len__(self) -> int:
        return len(self._decoders)

    def __iter__(self):
        return iter(self._decoders)