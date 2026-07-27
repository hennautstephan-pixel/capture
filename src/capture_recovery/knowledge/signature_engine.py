from __future__ import annotations

from collections.abc import Iterable

from capture_recovery.structures.structure import Structure

from .field_signature import FieldSignature
from .signature import Signature
from .signature_match import SignatureMatch
from .signature_registry import SignatureRegistry


class SignatureEngine:
    """
    Match reconstructed structures against semantic signatures.
    """

    def __init__(
        self,
        registry: SignatureRegistry,
    ) -> None:
        self.registry = registry

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def match(
        self,
        structure: Structure,
    ) -> tuple[SignatureMatch, ...]:
        """
        Match a structure against every registered signature.

        Results are sorted by descending score.
        """

        matches = [
            self._match_signature(structure, signature)
            for signature in self.registry
        ]

        matches.sort(
            key=lambda m: (
                m.score,
                m.percentage,
            ),
            reverse=True,
        )

        return tuple(matches)

    def best_match(
        self,
        structure: Structure,
    ) -> SignatureMatch | None:
        """
        Return the best signature match.
        """

        matches = self.match(structure)

        if not matches:
            return None

        return matches[0]

    def accepted_matches(
        self,
        structure: Structure,
    ) -> tuple[SignatureMatch, ...]:
        """
        Return only accepted matches.
        """

        return tuple(
            match
            for match in self.match(structure)
            if match.accepted
        )

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _match_signature(
        self,
        structure: Structure,
        signature: Signature,
    ) -> SignatureMatch:

        score = 0

        matched_required: list[str] = []

        matched_optional: list[str] = []

        missing_required: list[str] = []

        for expected in signature.required:

            if self._contains(structure, expected):

                matched_required.append(expected.name)

                score += expected.weight

            else:

                missing_required.append(expected.name)

        for expected in signature.optional:

            if self._contains(structure, expected):

                matched_optional.append(expected.name)

                score += expected.weight

        confidence = 0.0

        if signature.maximum_score > 0:

            confidence = score / signature.maximum_score

        return SignatureMatch(
            signature=signature,
            score=score,
            matched_required=tuple(matched_required),
            matched_optional=tuple(matched_optional),
            missing_required=tuple(missing_required),
            confidence=confidence,
        )

    def _contains(
        self,
        structure: Structure,
        expected: FieldSignature,
    ) -> bool:

        for field in structure.fields:

            dimensions = self._dimensions(field.value)

            if expected.matches(
                name=field.name,
                datatype=field.datatype,
                dimensions=dimensions,
            ):
                return True

        return False

    @staticmethod
    def _dimensions(
        value,
    ) -> int:
        """
        Infer the dimensionality of a field value.
        """

        if isinstance(value, tuple):
            return len(value)

        if isinstance(value, list):
            return len(value)

        return 1

    def __len__(self) -> int:
        return len(self.registry)

    def __bool__(self) -> bool:
        return len(self) > 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(signatures={len(self.registry)})"
        )