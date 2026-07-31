"""
Constraint merger.
"""

from __future__ import annotations

from collections import OrderedDict

from .confidence_aggregator import ConfidenceAggregator
from .property_candidate import PropertyCandidate


class ConstraintMerger:
    """
    Merges compatible PropertyCandidate instances into a single candidate.

    Candidates are merged only if they share the same identity
    (object type, property name, offset and value type).

    The resulting candidate:

    - aggregates confidence using ConfidenceAggregator;
    - keeps the maximum observation count;
    - combines all constraints without duplicates.
    """

    def __init__(self) -> None:
        self._aggregator = ConfidenceAggregator()

    def merge(
        self,
        candidates: list[PropertyCandidate],
    ) -> list[PropertyCandidate]:

        groups: OrderedDict[
            tuple[str, str, int, str],
            list[PropertyCandidate],
        ] = OrderedDict()

        for candidate in candidates:

            key = (
                candidate.object_type,
                candidate.property_name,
                candidate.offset,
                candidate.value_type,
            )

            groups.setdefault(key, []).append(candidate)

        merged: list[PropertyCandidate] = []

        for group in groups.values():

            constraints = []
            seen = set()

            for candidate in group:

                for constraint in candidate.constraints:

                    if constraint not in seen:
                        seen.add(constraint)
                        constraints.append(constraint)

            confidence = self._aggregator.aggregate(
                candidate.confidence
                for candidate in group
            )

            observations = max(
                candidate.observations
                for candidate in group
            )

            first = group[0]

            merged.append(
                PropertyCandidate(
                    object_type=first.object_type,
                    property_name=first.property_name,
                    offset=first.offset,
                    value_type=first.value_type,
                    confidence=confidence,
                    observations=observations,
                    constraints=tuple(constraints),
                )
            )

        return merged