"""
Boolean property correlator.
"""

from __future__ import annotations

from collections.abc import Sequence

from .correlation import Correlation
from .correlation_utils import (
    build_candidate,
    validate_observations,
)
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .value_type import ValueType


class BooleanCorrelator(Correlation):
    """
    Correlates boolean property observations.
    """

    PRIORITY = 100
    MIN_CONFIDENCE = 0.95

    @property
    def priority(self) -> int:
        """
        Execution priority.
        """

        return self.PRIORITY

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:
        """
        Analyse a collection of observations and produce a boolean
        property candidate.
        """

        if not all(
            isinstance(observation.semantic_before, bool)
            and isinstance(observation.semantic_after, bool)
            for observation in observations
        ):
            return None

        confidence = validate_observations(
            observations,
            min_confidence=self.MIN_CONFIDENCE,
        )

        if confidence is None:
            return None

        return build_candidate(
            observations,
            value_type=ValueType.BOOL,
            confidence=confidence,
        )