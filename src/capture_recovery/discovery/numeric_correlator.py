"""
Numeric property correlator.
"""

from __future__ import annotations

from collections.abc import Sequence

from .correlation import Correlation
from .property_candidate import PropertyCandidate
from .property_observation import PropertyObservation
from .value_type import ValueType


class NumericCorrelator(Correlation):
    """
    Correlates numeric property observations.
    """

    MIN_CONFIDENCE = 0.95

    def analyse(
        self,
        observations: Sequence[PropertyObservation],
    ) -> PropertyCandidate | None:

        if not observations:
            return None

        first = observations[0]

        consistent = sum(
            observation.is_consistent
            for observation in observations
        )

        confidence = consistent / len(observations)

        if confidence < self.MIN_CONFIDENCE:
            return None

        if not all(
            observation.object_type == first.object_type
            for observation in observations
        ):
            return None

        if not all(
            observation.offset == first.offset
            for observation in observations
        ):
            return None

        if not all(
            observation.semantic_property
            == first.semantic_property
            for observation in observations
        ):
            return None

        return PropertyCandidate(
            object_type=first.object_type,
            property_name=first.semantic_property,
            offset=first.offset,
            value_type=ValueType.FLOAT32,
            confidence=confidence,
            observations=len(observations),
        )
    