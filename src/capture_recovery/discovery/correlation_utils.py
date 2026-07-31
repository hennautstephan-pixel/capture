"""
Shared utilities for property correlators.
"""

from __future__ import annotations

from collections.abc import Sequence

from .property_candidate import PropertyCandidate
from .property_constraint import PropertyConstraint
from .property_observation import PropertyObservation
from .value_type import ValueType


def compute_confidence(
    observations: Sequence[PropertyObservation],
) -> float:
    """
    Compute the confidence score for a collection of observations.

    The score corresponds to the ratio of consistent observations.
    """

    if not observations:
        return 0.0

    consistent = sum(
        observation.is_consistent
        for observation in observations
    )

    return consistent / len(observations)


def validate_common_constraints(
    observations: Sequence[PropertyObservation],
) -> bool:
    """
    Validate that all observations refer to the same property.
    """

    if not observations:
        return False

    first = observations[0]

    if not all(
        observation.object_type == first.object_type
        for observation in observations
    ):
        return False

    if not all(
        observation.offset == first.offset
        for observation in observations
    ):
        return False

    if not all(
        observation.semantic_property == first.semantic_property
        for observation in observations
    ):
        return False

    return True


def validate_observations(
    observations: Sequence[PropertyObservation],
    *,
    min_confidence: float,
) -> float | None:
    """
    Validate a collection of observations.

    Returns
    -------
    float
        The computed confidence when the observations are valid.

    None
        If validation fails.
    """

    if not observations:
        return None

    if not validate_common_constraints(observations):
        return None

    confidence = compute_confidence(observations)

    if confidence < min_confidence:
        return None

    return confidence


def build_candidate(
    observations: Sequence[PropertyObservation],
    *,
    value_type: ValueType,
    confidence: float,
    constraints: Sequence[PropertyConstraint] = (),
) -> PropertyCandidate:
    """
    Build a PropertyCandidate from validated observations.
    """

    first = observations[0]

    return PropertyCandidate(
        object_type=first.object_type,
        property_name=first.semantic_property,
        offset=first.offset,
        value_type=value_type,
        confidence=confidence,
        observations=len(observations),
        constraints=tuple(constraints),
    )