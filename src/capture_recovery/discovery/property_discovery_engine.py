"""
Property discovery engine.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from .correlation import Correlation
from .discovery_result import DiscoveryResult
from .numeric_correlator import NumericCorrelator
from .property_observation import PropertyObservation


class PropertyDiscoveryEngine:
    """
    Discovers semantic properties from binary observations.
    """

    def __init__(
        self,
        correlators: Iterable[Correlation] | None = None,
    ) -> None:

        self._correlators = tuple(
            correlators
            if correlators is not None
            else (NumericCorrelator(),)
        )

    def discover(
        self,
        observations: Iterable[PropertyObservation],
    ) -> DiscoveryResult:
        """
        Analyse observations and discover property candidates.
        """

        observations = tuple(observations)

        groups: dict[
            tuple[str, int, str],
            list[PropertyObservation],
        ] = defaultdict(list)

        for observation in observations:

            key = (
                observation.object_type,
                observation.offset,
                observation.semantic_property,
            )

            groups[key].append(observation)

        candidates = []

        for group in groups.values():

            for correlator in self._correlators:

                candidate = correlator.analyse(group)

                if candidate is not None:
                    candidates.append(candidate)
                    break

        return DiscoveryResult(
            candidates=tuple(candidates),
            analysed_diffs=len(observations),
        )