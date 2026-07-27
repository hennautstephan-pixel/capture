"""
Models used by the diff engine.

These classes are immutable and represent the public API of the
capture_recovery.diff package.
"""

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Mapping
from typing import Sequence


class ChangeType(Enum):
    """Binary change classification."""

    INSERT = "insert"
    DELETE = "delete"
    MODIFY = "modify"
    MOVE = "move"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DiffChange:
    """
    Base class for every diff object.
    """

    offset: int

    confidence: float = 1.0

    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BinaryChange(DiffChange):
    """
    Represents one binary modification.
    """

    before: bytes = b""

    after: bytes = b""

    change_type: ChangeType = ChangeType.MODIFY

    @property
    def before_length(self) -> int:
        return len(self.before)

    @property
    def after_length(self) -> int:
        return len(self.after)

    @property
    def delta(self) -> int:
        return self.after_length - self.before_length


@dataclass(frozen=True, slots=True)
class RegionChange(DiffChange):
    """
    Represents changes affecting a memory region.
    """

    region: Any

    binary_changes: Sequence[BinaryChange] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class StructureChange(DiffChange):
    """
    Represents changes affecting one logical structure.
    """

    structure_before: Any | None = None

    structure_after: Any | None = None

    changed_fields: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class SemanticChange(DiffChange):
    """
    Represents a semantic modification.
    """

    object_type: str = ""

    object_identifier: str | int | None = None

    property_name: str = ""

    before: Any = None

    after: Any = None


@dataclass(frozen=True, slots=True)
class DiffStatistics:
    """
    Summary statistics.
    """

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


@dataclass(frozen=True, slots=True)
class DiffMetadata:
    """
    Report metadata.
    """

    project_before: str

    project_after: str

    created: datetime = field(default_factory=datetime.utcnow)

    tool_version: str = ""

    duration: float = 0.0


@dataclass(frozen=True, slots=True)
class DiffReport:
    """
    Complete diff report.
    """

    metadata: DiffMetadata

    statistics: DiffStatistics

    binary_changes: Sequence[BinaryChange] = field(default_factory=tuple)

    region_changes: Sequence[RegionChange] = field(default_factory=tuple)

    structure_changes: Sequence[StructureChange] = field(default_factory=tuple)

    semantic_changes: Sequence[SemanticChange] = field(default_factory=tuple)

    def is_empty(self) -> bool:
        return self.statistics.total_changes == 0

    def summary(self) -> str:
        return (
            f"{self.statistics.binary_changes} binary changes, "
            f"{self.statistics.region_changes} region changes, "
            f"{self.statistics.structure_changes} structure changes, "
            f"{self.statistics.semantic_changes} semantic changes"
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)