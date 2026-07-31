"""
Confidence aggregation.
"""

from __future__ import annotations

from collections.abc import Iterable


class ConfidenceAggregator:
    """
    Aggregates several confidence scores into a single confidence.

    The aggregation assumes that each confidence represents an
    independent probability.

    Formula:

        1 - Π(1 - confidence)
    """

    def aggregate(
        self,
        confidences: Iterable[float],
    ) -> float:

        product = 1.0
        found = False

        for confidence in confidences:

            found = True

            confidence = max(
                0.0,
                min(
                    1.0,
                    confidence,
                ),
            )

            product *= 1.0 - confidence

        if not found:
            return 0.0

        return 1.0 - product