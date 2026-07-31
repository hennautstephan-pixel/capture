"""
Correlator detecting numeric ranges.
"""

from __future__ import annotations

from collections.abc import Sequence

from .correlation import Correlation
from .correlation_utils import (
    build_candidate,
    validate_observations,
)
from .observation_statistics import ObservationStatistics
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .range_constraint import RangeConstraint
from .value_type import ValueType


class RangeCorrelator(Correlation):
    """
    Detect properties constrained to a numeric interval.
    """

    PRIORITY = 20

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

        if not (stats.all_integers or stats.all_floats):
            return None

        minimum = stats.minimum
        maximum = stats.maximum

        if minimum is None or maximum is None:
            return None

        if minimum == maximum:
            return None

        value_type = (
            ValueType.INT32
            if stats.all_integers
            else ValueType.FLOAT32
        )

        return build_candidate(
            observations,
            value_type=value_type,
            confidence=confidence,
            constraints=(
                RangeConstraint(
                    minimum=minimum,
                    maximum=maximum,
                ),
            ),
        )