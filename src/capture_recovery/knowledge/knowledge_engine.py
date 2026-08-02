from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.structures.structure import Structure

from .knowledge_result import KnowledgeResult
from .registry import DecoderRegistry
from .semantic_object import SemanticObject


class KnowledgeEngine:
    """
    Infer semantic objects from reconstructed structures.

    The legacy API (infer) is preserved for backwards
    compatibility while the new API (analyze) returns a
    complete KnowledgeResult.
    """

    def __init__(
        self,
        registry: DecoderRegistry,
    ) -> None:
        self.registry = registry

    def infer(
        self,
        structures: Iterable[Structure],
    ) -> tuple[SemanticObject, ...]:
        """
        Legacy API.

        Returns only decoded semantic objects.
        """

        return tuple(
            self.analyze(structures).decoded_objects
        )

    def analyze(
        self,
        structures: Iterable[Structure],
    ) -> KnowledgeResult:
        """
        Analyze reconstructed structures.

        Returns a complete KnowledgeResult.
        """

        result = KnowledgeResult()

        for structure in structures:

            decoded = False

            for decoder in self.registry:

                if not decoder.can_decode(structure):
                    continue

                obj = decoder.decode(structure)

                if obj is None:
                    continue

                result.add_known(structure)
                result.add_object(obj)
                result.add_signature(decoder)

                decoded = True
                break

            if not decoded:
                result.add_unknown(structure)

        return result