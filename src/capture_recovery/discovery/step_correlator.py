"""
Correlator detecting constant numeric steps.
"""

from __future__ import annotations

from collections.abc import Sequence
from math import gcd

from .correlation import Correlation
from .correlation_utils import (
    build_candidate,
    validate_observations,
)
from .observation_statistics import ObservationStatistics
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .step_constraint import StepConstraint
from .value_type import ValueType


class StepCorrelator(Correlation):

    PRIORITY = 25

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

        values = sorted(set(stats.semantic_values))

        if len(values) < 2:
            return None

        step = 0

        for a, b in zip(values, values[1:]):

            delta = b - a

            if delta == 0:
                continue

            if step == 0:
                step = delta
            else:
                step = gcd(step, delta)

        if step <= 1:
            return None

        return build_candidate(
            observations,
            value_type=ValueType.INT32,
            confidence=confidence,
            constraints=(
                StepConstraint(step),
            ),
        )