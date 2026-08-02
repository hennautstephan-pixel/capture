from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capture_recovery.knowledge import KnowledgeResult
from capture_recovery.structures import Structure


@dataclass(slots=True)
class InferenceContext:
    """
    Context shared by every inference rule.
    """

    #
    # Current structure
    #

    structure: Structure

    #
    # Optional knowledge
    #

    knowledge_result: KnowledgeResult | None = None

    #
    # Optional project
    #

    project: Any = None

    #
    # Options
    #

    options: dict[str, Any] = field(
        default_factory=dict,
    )

    #
    # Shared metadata
    #

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    # ---------------------------------------------------------
    # Structure
    # ---------------------------------------------------------

    @property
    def offset(self) -> int:
        return self.structure.offset

    @property
    def length(self) -> int:
        return self.structure.length

    @property
    def end(self) -> int:
        return self.structure.end

    @property
    def confidence(self) -> float:
        return self.structure.confidence

    @property
    def score(self) -> float:
        return self.structure.score

    @property
    def field_count(self) -> int:
        return len(self.structure.fields)

    # ---------------------------------------------------------
    # Knowledge
    # ---------------------------------------------------------

    @property
    def has_knowledge(self) -> bool:
        return self.knowledge_result is not None

    @property
    def knowledge_success(self) -> bool:

        if self.knowledge_result is None:
            return False

        return self.knowledge_result.success

    @property
    def coverage(self) -> float:

        if self.knowledge_result is None:
            return 0.0

        return self.knowledge_result.coverage

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.metadata.get(
            key,
            default,
        )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.metadata[key] = value

    # ---------------------------------------------------------
    # Options
    # ---------------------------------------------------------

    def option(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.options.get(
            key,
            default,
        )

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "InferenceContext("
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"score={self.score:.2f}, "
            f"knowledge={self.has_knowledge})"
        )