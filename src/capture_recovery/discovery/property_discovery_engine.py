"""
Property discovery engine.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

from .constraint_merger import ConstraintMerger
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
        self._constraint_merger = ConstraintMerger()

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

            group_candidates = []

            for correlator in self._registry.find_applicable(group):

                candidate = correlator.analyse(group)

                if candidate is not None:
                    group_candidates.append(candidate)

            if group_candidates:
                candidates.extend(
                    self._constraint_merger.merge(group_candidates)
                )

        return DiscoveryResult(
            candidates=tuple(candidates),
            analysed_diffs=len(observations),
        )