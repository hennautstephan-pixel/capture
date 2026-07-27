"""
Base semantic decoder.
"""

from __future__ import annotations

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.semantic_object import SemanticObject
from capture_recovery.knowledge.signature_engine import SignatureEngine
from capture_recovery.structures.structure import Structure


class BaseSemanticDecoder(Decoder):
    """
    Generic decoder based on a semantic signature.
    """

    object_type: str = ""

    def __init__(
        self,
        signature_engine: SignatureEngine,
    ) -> None:
        self.signature_engine = signature_engine

    def signature_name(self) -> str:
        """
        Return the expected signature name.
        """

        return self.object_type

    def can_decode(
        self,
        structure: Structure,
    ) -> bool:
        """
        Check if structure matches this decoder.
        """

        match = self.signature_engine.best_match(
            structure,
        )

        if match is None:
            return False

        return (
            match.accepted
            and match.signature.name == self.signature_name()
        )

    def decode(
        self,
        structure: Structure,
    ) -> SemanticObject | None:
        """
        Decode a structure into a semantic object.
        """

        match = self.signature_engine.best_match(
            structure,
        )

        if match is None:
            return None

        if not match.accepted:
            return None

        if match.signature.name != self.signature_name():
            return None

        properties = {
            field.name: field.value
            for field in structure.fields
        }

        identifier = self.identifier(
            properties,
        )

        return SemanticObject(
            object_type=self.object_type,
            identifier=identifier,
            properties=properties,
            confidence=match.confidence,
        )

    def identifier(
        self,
        properties: dict,
    ) -> str | int:
        """
        Default identifier strategy.
        """

        return properties.get(
            "name",
            "unknown",
        )