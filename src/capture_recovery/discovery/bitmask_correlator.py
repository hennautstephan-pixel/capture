"""
Correlator detecting bitmask properties.
"""

from __future__ import annotations

from collections.abc import Sequence

from .bitmask_constraint import BitmaskConstraint
from .correlation import Correlation
from .correlation_utils import (
    build_candidate,
    validate_observations,
)
from .observation_statistics import ObservationStatistics
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .value_type import ValueType


class BitmaskCorrelator(Correlation):
    """
    Detects integer properties behaving like bitmasks.
    """

    PRIORITY = 30

    MIN_OBSERVATIONS = 5
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

        values = list(stats.semantic_values)

        if len(set(values)) < 2:
            return None

        mask = 0

        for value in values:

            if value < 0:
                return None

            mask |= value

        # Nothing to infer.
        if mask == 0:
            return None

        return build_candidate(
            observations,
            value_type=ValueType.INT32,
            confidence=confidence,
            constraints=(
                BitmaskConstraint(mask),
            ),
        )