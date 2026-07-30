"""
Factory for creating and decoding semantic objects.
"""

from __future__ import annotations

from capture_recovery.structures.structure import Structure

from .knowledge_registry import KnowledgeRegistry
from .semantic_object import SemanticObject


class ObjectFactory:
    """
    Create semantic objects using the knowledge registry.
    """

    def __init__(
        self,
        registry: KnowledgeRegistry,
    ) -> None:
        self.registry: KnowledgeRegistry = registry

    def create(
        self,
        name: str,
        identifier: str,
    ) -> SemanticObject:
        """
        Create an empty semantic object.
        """

        if name not in self.registry:
            raise KeyError(
                f"Unknown object type '{name}'."
            )

        return SemanticObject(
            object_type=name,
            identifier=identifier,
        )

    def decode(
        self,
        name: str,
        structure: Structure,
    ) -> SemanticObject | None:
        """
        Decode a structure using the registered decoder.
        """

        decoder = self.registry.decoder_for(name)

        if not decoder.can_decode(structure):
            return None

        return decoder.decode(structure)