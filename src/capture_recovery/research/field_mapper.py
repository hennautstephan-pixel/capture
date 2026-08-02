from __future__ import annotations

from dataclasses import dataclass

from .structure_mapper import (
    CandidateStructure,
    StructureMap,
)


@dataclass(slots=True, frozen=True)
class FieldCandidate:
    """
    Candidate field extracted from a candidate structure.

    At this stage, the field has no confirmed semantic
    meaning. It only represents a region that may encode
    a value.
    """

    offset: int

    length: int

    confidence: float

    evidence: tuple[str, ...]

    #
    # Keep the public API simple.
    # Rich typing can be added later without
    # breaking existing code.
    #
    type_candidates: tuple[str, ...]

    name: str | None = None

    @property
    def end(self) -> int:
        return self.offset + self.length


@dataclass(slots=True, frozen=True)
class FieldMap:
    """
    Collection of candidate fields.
    """

    fields: list[FieldCandidate]

    @property
    def field_count(self) -> int:
        return len(self.fields)

    def by_offset(self) -> list[FieldCandidate]:

        return sorted(
            self.fields,
            key=lambda field: (
                field.offset,
                field.length,
            ),
        )


class FieldMapper:
    """
    Convert candidate structures into candidate fields.

    This mapper does not attempt to identify the exact
    semantic meaning of a field.

    It only proposes possible binary value types.
    """

    def map(
        self,
        structures: StructureMap,
    ) -> FieldMap:

        fields: list[FieldCandidate] = []

        for structure in structures.by_offset():

            fields.append(
                FieldCandidate(
                    offset=structure.offset,
                    length=structure.length,
                    confidence=structure.confidence,
                    evidence=structure.evidence,
                    type_candidates=self._candidate_types(
                        structure.length,
                    ),
                    name=structure.name,
                )
            )

        return FieldMap(fields)

    @staticmethod
    def _candidate_types(
        length: int,
    ) -> tuple[str, ...]:
        """
        Return possible binary types for a field.

        These are hypotheses only.
        """

        candidates: list[str] = [
            "bytes",
        ]

        if length == 1:

            candidates.extend(
                (
                    "bool",
                    "uint8",
                    "int8",
                )
            )

        elif length == 2:

            candidates.extend(
                (
                    "uint16",
                    "int16",
                )
            )

        elif length == 4:

            candidates.extend(
                (
                    "uint32",
                    "int32",
                    "float32",
                )
            )

        elif length == 8:

            candidates.extend(
                (
                    "uint64",
                    "int64",
                    "float64",
                )
            )

        elif length == 16:

            candidates.append(
                "guid"
            )

        return tuple(candidates)