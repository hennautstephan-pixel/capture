"""
Property discovery engine.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from .correlator_registry import CorrelatorRegistry
from .discovery_result import DiscoveryResult
from .numeric_correlator import NumericCorrelator
from .property_observation import PropertyObservation


class PropertyDiscoveryEngine:
    """
    Discovers semantic properties from binary observations.
    """

    def __init__(
        self,
        registry: CorrelatorRegistry | None = None,
    ) -> None:

        if registry is None:
            registry = CorrelatorRegistry(
                [
                    NumericCorrelator(),
                ]
            )

        self._registry = registry

    @property
    def registry(self) -> CorrelatorRegistry:
        """
        Returns the correlator registry used by the engine.
        """
        return self._registry

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

            for correlator in self._registry.find_applicable(group):

                candidate = correlator.analyse(group)

                if candidate is not None:
                    candidates.append(candidate)
                    break

        return DiscoveryResult(
            candidates=tuple(candidates),
            analysed_diffs=len(observations),
        )