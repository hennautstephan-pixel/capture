from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.structures.structure import Structure

from .registry import DecoderRegistry
from .semantic_object import SemanticObject


class KnowledgeEngine:

    def __init__(
        self,
        registry: DecoderRegistry,
    ) -> None:
        self.registry = registry

    def infer(
        self,
        structures: Iterable[Structure],
    ) -> tuple[SemanticObject, ...]:

        objects: list[SemanticObject] = []

        for structure in structures:

            for decoder in self.registry:

                if not decoder.can_decode(structure):
                    continue

                obj = decoder.decode(structure)

                if obj is not None:
                    objects.append(obj)

        return tuple(objects)