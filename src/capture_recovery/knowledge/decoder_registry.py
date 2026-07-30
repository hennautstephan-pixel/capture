"""
Registry of generated decoders.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.semantic_object import SemanticObject


class DecoderRegistry:
    """
    Registry of semantic object decoders.
    """

    def __init__(
        self,
        decoders: Mapping[str, Decoder] | None = None,
    ) -> None:
        self._decoders: dict[str, Decoder] = dict(decoders or {})

    def register(
        self,
        name: str,
        decoder: Decoder,
    ) -> None:
        """
        Register a decoder.
        """

        self._decoders[name] = decoder

    def decoder_for(
        self,
        name: str,
    ) -> Decoder:
        """
        Return the decoder registered for an object.
        """

        try:
            return self._decoders[name]
        except KeyError as exc:
            raise KeyError(
                f"No decoder registered for '{name}'."
            ) from exc

    def decode(
        self,
        name: str,
        reader,
    ) -> SemanticObject:
        """
        Decode an object using its registered decoder.
        """

        return self.decoder_for(name).decode(reader)

    def __contains__(
        self,
        name: object,
    ) -> bool:
        return name in self._decoders

    def __len__(self) -> int:
        return len(self._decoders)

    def __iter__(self) -> Iterator[str]:
        return iter(self._decoders)

    @property
    def names(self) -> tuple[str, ...]:
        """
        Registered object names.
        """

        return tuple(sorted(self._decoders))