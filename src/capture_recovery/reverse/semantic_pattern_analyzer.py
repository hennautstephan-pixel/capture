from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from capture_recovery.reverse.semantic_diff import DiffKind, SemanticDiff, ValueDifference


@dataclass(frozen=True, slots=True)
class PatternObservation:
    """A measurable observation about recurring semantic-diff patterns."""

    pattern_id: str
    description: str
    value_type: str
    offsets: tuple[int, ...]
    occurrences: int
    confidence: float


@dataclass(frozen=True, slots=True)
class PatternReport:
    """A summary of recurring pattern observations over a series of diffs."""

    observations: tuple[PatternObservation, ...]
    statistics: dict[str, int | float]


class SemanticPatternAnalyzer:
    """Discover objective, measurable patterns in a collection of SemanticDiff objects."""

    def analyze(self, diffs: Iterable[SemanticDiff]) -> PatternReport:
        """Aggregate recurring patterns from one or more semantic diffs.

        The V1 implementation stays intentionally factual: it reports the most
        common modified offsets, the most frequent value types involved in
        changes, the number of additions/removals/modifications, and the size
        distribution of observed values. No business hypothesis is inferred.
        """
        diff_list = list(diffs)
        all_changes = [difference for diff in diff_list for difference in self._iter_changes(diff)]

        modified_offsets = tuple(sorted({self._offset_of(difference) for difference in all_changes if self._offset_of(difference) is not None}))
        offset_groups: Counter[tuple[int, ...]] = Counter()
        for diff in diff_list:
            offsets = tuple(sorted({self._offset_of(change) for change in self._iter_changes(diff) if self._offset_of(change) is not None}))
            if len(offsets) > 1:
                offset_groups[offsets] += 1

        type_counter: Counter[str] = Counter(self._value_type(change) for change in all_changes)
        size_counter: Counter[int] = Counter(self._value_size(change) for change in all_changes)
        kind_counter: Counter[str] = Counter(change.kind.name for change in all_changes)

        observations: list[PatternObservation] = []
        if modified_offsets:
            observations.append(
                PatternObservation(
                    pattern_id="modified_offsets",
                    description="Offsets appearing in semantic changes",
                    value_type="mixed",
                    offsets=modified_offsets,
                    occurrences=len(modified_offsets),
                    confidence=1.0,
                )
            )

        for value_type, count in sorted(type_counter.items(), key=lambda item: (-item[1], item[0])):
            if count > 0:
                observations.append(
                    PatternObservation(
                        pattern_id=f"type_{value_type}",
                        description="Most frequent changed value types",
                        value_type=value_type,
                        offsets=tuple(sorted({self._offset_of(change) for change in all_changes if self._value_type(change) == value_type})),
                        occurrences=count,
                        confidence=count / len(all_changes) if all_changes else 0.0,
                    )
                )

        for offsets, count in sorted(offset_groups.items(), key=lambda item: (item[1], item[0])):
            observations.append(
                PatternObservation(
                    pattern_id=f"offset_group_{len(offsets)}",
                    description="Recurring offset group observed together",
                    value_type="mixed",
                    offsets=offsets,
                    occurrences=count,
                    confidence=count / len(diff_list) if diff_list else 0.0,
                )
            )

        if size_counter:
            dominant_size = max(size_counter.items(), key=lambda item: (item[1], -item[0]))[0]
            observations.append(
                PatternObservation(
                    pattern_id="dominant_size",
                    description="Most common value size observed in changes",
                    value_type="mixed",
                    offsets=tuple(sorted({self._offset_of(change) for change in all_changes if self._value_size(change) == dominant_size})),
                    occurrences=size_counter[dominant_size],
                    confidence=size_counter[dominant_size] / len(all_changes) if all_changes else 0.0,
                )
            )

        statistics = {
            "semantic_diff_count": len(diff_list),
            "total_changed_values": len(all_changes),
            "unique_offsets": len(modified_offsets),
            "detected_groups": len(offset_groups) if diff_list else 0,
            "diff_kind_frequency": {kind: kind_counter.get(kind, 0) for kind in (DiffKind.ADDED.name, DiffKind.REMOVED.name, DiffKind.MODIFIED.name, DiffKind.UNCHANGED.name)},
            "value_type_frequency": dict(sorted(type_counter.items(), key=lambda item: item[0])),
        }

        return PatternReport(observations=tuple(observations), statistics=statistics)

    def _iter_changes(self, diff: SemanticDiff) -> tuple[ValueDifference, ...]:
        return diff.added + diff.removed + diff.modified + diff.unchanged

    def _offset_of(self, difference: ValueDifference) -> int | None:
        if difference.before is not None:
            return difference.before.offset
        if difference.after is not None:
            return difference.after.offset
        return None

    def _value_type(self, difference: ValueDifference) -> str:
        if difference.before is not None:
            return difference.before.type
        if difference.after is not None:
            return difference.after.type
        return ""

    def _value_size(self, difference: ValueDifference) -> int:
        if difference.before is not None:
            return difference.before.size
        if difference.after is not None:
            return difference.after.size
        return 0


__all__ = ["PatternObservation", "PatternReport", "SemanticPatternAnalyzer"]
