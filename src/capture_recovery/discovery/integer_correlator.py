"""
Integer property correlator.
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
from .value_type import ValueType


class IntegerCorrelator(Correlation):
    """
    Correlates integer property observations.
    """

    PRIORITY = 20
    MIN_CONFIDENCE = 0.95

    @property
    def priority(self) -> int:
        """
        Execution priority.

        Integer correlation executes before the generic numeric
        correlator but after specialised correlators such as Boolean.
        """
        return self.PRIORITY

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:
        """
        Analyse a collection of observations and produce an integer
        property candidate.
        """

        stats = ObservationStatistics(observations)

        if not stats.all_integers:
            return None

        confidence = validate_observations(
            observations,
            min_confidence=self.MIN_CONFIDENCE,
        )

        if confidence is None:
            return None

        return build_candidate(
            observations,
            value_type=ValueType.INT32,
            confidence=confidence,
        )