from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol, TypeVar

from capture_recovery.core.recovered_value import RecoveredValue


class DiffKind(Enum):
    """Describe the semantic relationship between two recovered values."""

    UNCHANGED = "unchanged"
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"


@dataclass(frozen=True, slots=True)
class ValueDifference:
    """Represents a single semantic difference between two recovered values."""

    kind: DiffKind
    before: RecoveredValue | None = None
    after: RecoveredValue | None = None


@dataclass(frozen=True, slots=True)
class SemanticDiff:
    """Container for all semantic differences between two recovered-value sets."""

    added: tuple[ValueDifference, ...]
    removed: tuple[ValueDifference, ...]
    modified: tuple[ValueDifference, ...]
    unchanged: tuple[ValueDifference, ...]


class ComparisonStrategy(Protocol):
    """Strategy used to determine whether two recovered values match."""

    def match_key(self, value: RecoveredValue) -> tuple[object, ...]:
        """Return a stable key used to associate values across the two sets."""

    def is_equal(self, before: RecoveredValue, after: RecoveredValue) -> bool:
        """Return whether two values are semantically identical for this strategy."""


class DefaultComparisonStrategy:
    """Default comparison strategy based on offset, type, size, and value."""

    def match_key(self, value: RecoveredValue) -> tuple[object, ...]:
        return (value.offset, value.type)

    def is_equal(self, before: RecoveredValue, after: RecoveredValue) -> bool:
        return (
            before.offset == after.offset
            and before.type == after.type
            and before.size == after.size
            and before.value == after.value
        )


class SemanticDiffEngine:
    """Compare two recovered-value collections without inspecting raw bytes."""

    def __init__(self, strategy: ComparisonStrategy | None = None) -> None:
        """Initialize the engine with an optional comparison strategy.

        Args:
            strategy: Optional pluggable strategy for matching and equality.
                When omitted, the default strategy compares offset, type, size,
                and value.
        """
        self._strategy = strategy or DefaultComparisonStrategy()

    def compare(
        self,
        before: Iterable[RecoveredValue],
        after: Iterable[RecoveredValue],
    ) -> SemanticDiff:
        """Compare two recovered-value iterables and classify the differences.

        The comparison is deterministic and side-effect free. Each value from the
        ``before`` collection is matched against the ``after`` collection using a
        stable key and then classified as unchanged, modified, or removed. Any
        values that only appear in ``after`` are reported as added.
        """
        before_values = list(before)
        after_values = list(after)

        before_by_key: dict[tuple[object, ...], list[RecoveredValue]] = {}
        for value in before_values:
            before_by_key.setdefault(self._strategy.match_key(value), []).append(value)

        after_by_key: dict[tuple[object, ...], list[RecoveredValue]] = {}
        for value in after_values:
            after_by_key.setdefault(self._strategy.match_key(value), []).append(value)

        added: list[ValueDifference] = []
        removed: list[ValueDifference] = []
        modified: list[ValueDifference] = []
        unchanged: list[ValueDifference] = []

        keys = list(dict.fromkeys([self._strategy.match_key(value) for value in before_values] + [self._strategy.match_key(value) for value in after_values]))

        for key in keys:
            before_group = before_by_key.get(key, [])
            after_group = after_by_key.get(key, [])

            while before_group and after_group:
                before_value = before_group.pop(0)
                after_value = after_group.pop(0)
                if self._strategy.is_equal(before_value, after_value):
                    unchanged.append(ValueDifference(kind=DiffKind.UNCHANGED, before=before_value, after=after_value))
                else:
                    modified.append(ValueDifference(kind=DiffKind.MODIFIED, before=before_value, after=after_value))

            for value in before_group:
                removed.append(ValueDifference(kind=DiffKind.REMOVED, before=value, after=None))

            for value in after_group:
                added.append(ValueDifference(kind=DiffKind.ADDED, before=None, after=value))

        return SemanticDiff(
            added=tuple(added),
            removed=tuple(removed),
            modified=tuple(modified),
            unchanged=tuple(unchanged),
        )


__all__ = ["DiffKind", "ValueDifference", "SemanticDiff", "ComparisonStrategy", "SemanticDiffEngine"]
