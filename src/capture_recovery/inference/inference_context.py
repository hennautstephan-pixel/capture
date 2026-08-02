from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capture_recovery.knowledge import KnowledgeResult
from capture_recovery.structures import Structure


@dataclass(slots=True)
class InferenceContext:
    """
    Context shared by every inference rule.

    The context is intentionally lightweight. It carries every piece of
    information that inference rules may need while recovering a Capture
    project and also provides a shared workspace where rules can exchange
    information.
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
    # Engine options
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

    #
    # Shared cache
    #

    cache: dict[str, Any] = field(
        default_factory=dict,
    )

    #
    # Diagnostics
    #

    warnings: list[str] = field(
        default_factory=list,
    )

    notes: list[str] = field(
        default_factory=list,
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

    def has_option(
        self,
        key: str,
    ) -> bool:

        return key in self.options

    # ---------------------------------------------------------
    # Shared cache
    # ---------------------------------------------------------

    def cache_get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self.cache.get(
            key,
            default,
        )

    def cache_set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.cache[key] = value

    # ---------------------------------------------------------
    # Diagnostics
    # ---------------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)

    def add_note(
        self,
        message: str,
    ) -> None:

        self.notes.append(message)

    # ---------------------------------------------------------
    # Representation
    # ---------------------------------------------------------

    def __repr__(self) -> str:

        return (
            "InferenceContext("
            f"offset=0x{self.offset:X}, "
            f"length={self.length}, "
            f"score={self.score:.2f}, "
            f"knowledge={self.has_knowledge}, "
            f"warnings={len(self.warnings)}, "
            f"notes={len(self.notes)})"
        )