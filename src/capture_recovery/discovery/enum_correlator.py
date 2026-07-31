"""
Correlator detecting enumerated integer properties.
"""

from __future__ import annotations

from collections.abc import Sequence

from .correlation import Correlation
from .correlation_utils import (
    build_candidate,
    validate_observations,
)
from .enum_constraint import EnumConstraint
from .observation_statistics import ObservationStatistics
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .value_type import ValueType


class EnumCorrelator(Correlation):
    """
    Detect properties whose values belong to a small finite set.
    """

    PRIORITY = 40

    MIN_OBSERVATIONS = 5
    MAX_ENUM_VALUES = 8
    MIN_CONFIDENCE = 0.95

    @property
    def priority(self) -> int:
        return self.PRIORITY

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:

        if len(observations) < self.MIN_OBSERVATIONS:
            return None

        confidence = validate_observations(
            observations,
            min_confidence=self.MIN_CONFIDENCE,
        )

        if confidence is None:
            return None

        stats = ObservationStatistics(observations)

        if not stats.all_integers:
            return None

        distinct = tuple(sorted(stats.distinct_semantic_values))

        if len(distinct) <= 1:
            return None

        if len(distinct) > self.MAX_ENUM_VALUES:
            return None

        return build_candidate(
            observations,
            value_type=ValueType.INT32,
            confidence=confidence,
            constraints=(
                EnumConstraint(distinct),
            ),
        )