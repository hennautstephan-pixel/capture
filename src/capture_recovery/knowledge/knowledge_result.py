"""
Knowledge engine result.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class KnowledgeResult:
    """
    Result produced by the knowledge engine.

    It stores every recognised structure,
    unknown structure, decoded object and
    signature match generated during the
    knowledge phase.
    """

    #
    # Structures
    #

    known_structures: list[Any] = field(
        default_factory=list,
    )

    unknown_structures: list[Any] = field(
        default_factory=list,
    )

    #
    # Semantic objects
    #

    decoded_objects: list[Any] = field(
        default_factory=list,
    )

    #
    # Signature matches
    #

    signature_matches: list[Any] = field(
        default_factory=list,
    )

    #
    # Metadata
    #

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def known_signature_count(self) -> int:
        """
        Number of recognised structures.
        """

        return len(
            self.known_structures,
        )

    @property
    def unknown_signature_count(self) -> int:
        """
        Number of unknown structures.
        """

        return len(
            self.unknown_structures,
        )

    @property
    def decoded_object_count(self) -> int:
        """
        Number of decoded semantic objects.
        """

        return len(
            self.decoded_objects,
        )

    @property
    def signature_count(self) -> int:
        """
        Number of signature matches.
        """

        return len(
            self.signature_matches,
        )

    @property
    def total(self) -> int:
        """
        Total analysed structures.
        """

        return (
            self.known_signature_count
            + self.unknown_signature_count
        )

    @property
    def coverage(self) -> float:
        """
        Recognition coverage.
        """

        total = self.total

        if total == 0:
            return 0.0

        return (
            self.known_signature_count
            / total
        )

    @property
    def success(self) -> bool:
        """
        True if at least one structure
        has been recognised.
        """

        return (
            self.known_signature_count > 0
        )

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add_known(
        self,
        structure: Any,
    ) -> None:
        """
        Register a recognised structure.
        """

        self.known_structures.append(
            structure,
        )

    def add_unknown(
        self,
        structure: Any,
    ) -> None:
        """
        Register an unknown structure.
        """

        self.unknown_structures.append(
            structure,
        )

    def add_object(
        self,
        obj: Any,
    ) -> None:
        """
        Register a decoded semantic object.
        """

        self.decoded_objects.append(
            obj,
        )

    def add_signature(
        self,
        match: Any,
    ) -> None:
        """
        Register a signature match.
        """

        self.signature_matches.append(
            match,
        )

    def clear(self) -> None:
        """
        Clear every collected result.
        """

        self.known_structures.clear()
        self.unknown_structures.clear()
        self.decoded_objects.clear()
        self.signature_matches.clear()
        self.metadata.clear()

    # ------------------------------------------------------------------
    # Python protocol
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        return self.total

    def __bool__(self) -> bool:
        return self.success