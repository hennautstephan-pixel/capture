"""
Immutable models used by the diff engine.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import UTC
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Mapping


Metadata = Mapping[str, Any]


class ChangeType(Enum):
    """Type of binary change."""

    INSERT = "insert"
    DELETE = "delete"
    MODIFY = "modify"
    MOVE = "move"
    UNKNOWN = "unknown"


# ============================================================================
# Binary
# ============================================================================


@dataclass(frozen=True, slots=True)
class BinaryChange:
    """Represents one binary modification."""

    offset: int

    before: bytes = b""

    after: bytes = b""

    change_type: ChangeType = ChangeType.MODIFY

    confidence: float = 1.0

    metadata: Metadata = field(
        default_factory=dict,
        compare=False,
        hash=False,
        repr=False,
    )

    @property
    def before_length(self) -> int:
        return len(self.before)

    @property
    def after_length(self) -> int:
        return len(self.after)

    @property
    def delta(self) -> int:
        return self.after_length - self.before_length


# ============================================================================
# Region
# ============================================================================


@dataclass(frozen=True, slots=True)
class RegionChange:
    """Represents modifications inside one memory region."""

    offset: int

    region: Any

    binary_changes: tuple[BinaryChange, ...] = ()

    confidence: float = 1.0

    metadata: Metadata = field(
        default_factory=dict,
        compare=False,
        hash=False,
        repr=False,
    )


# ============================================================================
# Structure
# ============================================================================


@dataclass(frozen=True, slots=True)
class StructureChange:
    """Represents modifications affecting one logical structure."""

    offset: int

    structure_before: Any | None = None

    structure_after: Any | None = None

    changed_fields: tuple[str, ...] = ()

    confidence: float = 1.0

    metadata: Metadata = field(
        default_factory=dict,
        compare=False,
        hash=False,
        repr=False,
    )


# ============================================================================
# Semantic
# ============================================================================


@dataclass(frozen=True, slots=True)
class SemanticChange:
    """Represents one semantic modification."""

    offset: int

    object_type: str = ""

    object_identifier: str | int | None = None

    property_name: str = ""

    before: Any = None

    after: Any = None

    confidence: float = 1.0

    metadata: Metadata = field(
        default_factory=dict,
        compare=False,
        hash=False,
        repr=False,
    )


# ============================================================================
# Statistics
# ============================================================================


@dataclass(frozen=True, slots=True)
class DiffStatistics:
    """Summary of detected changes."""

    bytes_added: int = 0

    bytes_removed: int = 0

    bytes_modified: int = 0

    binary_changes: int = 0

    region_changes: int = 0

    structure_changes: int = 0

    semantic_changes: int = 0

    @property
    def total_changes(self) -> int:
        return (
            self.binary_changes
            + self.region_changes
            + self.structure_changes
            + self.semantic_changes
        )

    # ============================================================================
# Metadata
# ============================================================================


@dataclass(frozen=True, slots=True)
class DiffMetadata:
    """Metadata associated with a diff report."""

    project_before: str

    project_after: str

    created: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    tool_version: str = ""

    duration: float = 0.0

    @property
    def project_name_before(self) -> str:
        return self.project_before

    @property
    def project_name_after(self) -> str:
        return self.project_after


# ============================================================================
# Report
# ============================================================================


@dataclass(frozen=True, slots=True)
class DiffReport:
    """Complete diff report."""

    metadata: DiffMetadata

    statistics: DiffStatistics

    binary_changes: tuple[BinaryChange, ...] = ()

    region_changes: tuple[RegionChange, ...] = ()

    structure_changes: tuple[StructureChange, ...] = ()

    semantic_changes: tuple[SemanticChange, ...] = ()

    def is_empty(self) -> bool:
        """Return True when no changes are present."""
        return self.statistics.total_changes == 0

    @property
    def total_changes(self) -> int:
        """Shortcut to the statistics."""
        return self.statistics.total_changes

    def summary(self) -> str:
        """Return a short human-readable summary."""
        return (
            f"{self.statistics.binary_changes} binary changes, "
            f"{self.statistics.region_changes} region changes, "
            f"{self.statistics.structure_changes} structure changes, "
            f"{self.statistics.semantic_changes} semantic changes"
        )

    def __len__(self) -> int:
        return self.statistics.total_changes

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __iter__(self):
        yield from self.binary_changes
        yield from self.region_changes
        yield from self.structure_changes
        yield from self.semantic_changes

    def binary_at(self, offset: int) -> BinaryChange | None:
        """Return the binary change at a given offset."""
        for change in self.binary_changes:
            if change.offset == offset:
                return change
        return None

    def semantic_of_type(
        self,
        object_type: str,
    ) -> tuple[SemanticChange, ...]:
        """Return semantic changes matching an object type."""
        return tuple(
            change
            for change in self.semantic_changes
            if change.object_type == object_type
        )

    def filter_confidence(
        self,
        minimum: float,
    ) -> "DiffReport":
        """Return a report filtered by minimum confidence."""

        return DiffReport(
            metadata=self.metadata,
            statistics=self.statistics,
            binary_changes=tuple(
                c for c in self.binary_changes
                if c.confidence >= minimum
            ),
            region_changes=tuple(
                c for c in self.region_changes
                if c.confidence >= minimum
            ),
            structure_changes=tuple(
                c for c in self.structure_changes
                if c.confidence >= minimum
            ),
            semantic_changes=tuple(
                c for c in self.semantic_changes
                if c.confidence >= minimum
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert the report into a JSON-serializable dictionary."""

        return {
            "metadata": {
                "project_before": self.metadata.project_before,
                "project_after": self.metadata.project_after,
                "created": self.metadata.created.isoformat(),
                "tool_version": self.metadata.tool_version,
                "duration": self.metadata.duration,
            },
            "statistics": asdict(self.statistics),
            "binary_changes": [
                {
                    "offset": change.offset,
                    "before": change.before.hex(),
                    "after": change.after.hex(),
                    "change_type": change.change_type.value,
                    "confidence": change.confidence,
                }
                for change in self.binary_changes
            ],
            "region_changes": [
                asdict(change)
                for change in self.region_changes
            ],
            "structure_changes": [
                asdict(change)
                for change in self.structure_changes
            ],
            "semantic_changes": [
                asdict(change)
                for change in self.semantic_changes
            ],
        }