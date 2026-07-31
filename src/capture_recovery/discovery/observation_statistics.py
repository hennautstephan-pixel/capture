"""
Statistics computed from a collection of property observations.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from .property_observation import PropertyObservation


@dataclass(frozen=True, slots=True)
class ObservationStatistics:
    """
    Summary statistics for a collection of PropertyObservation objects.
    """

    observations: Sequence[PropertyObservation]

    @property
    def count(self) -> int:
        """
        Number of observations.
        """
        return len(self.observations)

    @property
    def semantic_values(self) -> tuple[Any, ...]:
        """
        Semantic values observed after modification.
        """
        return tuple(
            observation.semantic_after
            for observation in self.observations
        )

    @property
    def binary_values(self) -> tuple[Any, ...]:
        """
        Binary values observed after modification.
        """
        return tuple(
            observation.binary_after
            for observation in self.observations
        )

    @property
    def distinct_semantic_values(self) -> frozenset[Any]:
        """
        Distinct semantic values.
        """
        return frozenset(self.semantic_values)

    @property
    def distinct_binary_values(self) -> frozenset[Any]:
        """
        Distinct binary values.
        """
        return frozenset(self.binary_values)

    @property
    def semantic_value_count(self) -> int:
        """
        Number of distinct semantic values.
        """
        return len(self.distinct_semantic_values)

    @property
    def binary_value_count(self) -> int:
        """
        Number of distinct binary values.
        """
        return len(self.distinct_binary_values)

    @property
    def all_booleans(self) -> bool:
        """
        True if all semantic values are bool.
        """
        return all(
            isinstance(value, bool)
            for value in self.semantic_values
        )

    @property
    def all_integers(self) -> bool:
        """
        True if all semantic values are integers (excluding bool).
        """
        return all(
            isinstance(value, int)
            and not isinstance(value, bool)
            for value in self.semantic_values
        )

    @property
    def all_floats(self) -> bool:
        """
        True if all semantic values are floats.
        """
        return all(
            isinstance(value, float)
            for value in self.semantic_values
        )

    @property
    def all_strings(self) -> bool:
        """
        True if all semantic values are strings.
        """
        return all(
            isinstance(value, str)
            for value in self.semantic_values
        )

    @property
    def minimum(self) -> Any | None:
        """
        Minimum semantic value when comparable.
        """
        if not self.semantic_values:
            return None

        try:
            return min(self.semantic_values)
        except TypeError:
            return None

    @property
    def maximum(self) -> Any | None:
        """
        Maximum semantic value when comparable.
        """
        if not self.semantic_values:
            return None

        try:
            return max(self.semantic_values)
        except TypeError:
            return None

    @property
    def is_small_integer_domain(self) -> bool:
        """
        True when observations appear to belong to a small integer domain.

        This heuristic is intended for future EnumCorrelator support.
        """

        if not self.all_integers:
            return False

        return (
            self.semantic_value_count <= 16
            and self.minimum is not None
            and self.maximum is not None
            and (self.maximum - self.minimum) <= 32
        )