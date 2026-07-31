"""
Registry of discovery correlators.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Tuple

from .correlation import Correlation
from .property_observation import PropertyObservation


class CorrelatorRegistry:
    """
    Registry containing all available correlators.

    Correlators are always kept ordered by descending priority.
    """

    def __init__(
        self,
        correlators: Iterable[Correlation] | None = None,
    ) -> None:

        self._correlators: list[Correlation] = []

        if correlators is not None:
            for correlator in correlators:
                self.register(correlator)

    @property
    def correlators(self) -> Tuple[Correlation, ...]:
        """
        Returns the registered correlators ordered by priority.
        """
        return tuple(self._correlators)

    def register(
        self,
        correlator: Correlation,
    ) -> None:
        """
        Registers a correlator.

        Duplicate registrations are ignored.
        """

        if correlator in self._correlators:
            return

        self._correlators.append(correlator)

        self._correlators.sort(
            key=lambda c: c.priority,
            reverse=True,
        )

    def unregister(
        self,
        correlator: Correlation,
    ) -> None:
        """
        Removes a correlator.

        Raises
        ------
        ValueError
            If the correlator is not registered.
        """

        self._correlators.remove(correlator)

    def clear(self) -> None:
        """
        Removes every registered correlator.
        """

        self._correlators.clear()

    def ordered(self) -> tuple[Correlation, ...]:
        """
        Returns correlators ordered by descending priority.
        """

        return tuple(self._correlators)

    def find_applicable(
        self,
        observations: Iterable[PropertyObservation],
    ) -> tuple[Correlation, ...]:
        """
        Returns correlators applicable to the supplied observations.

        At the moment every registered correlator is returned.
        Future versions may filter according to the observation type.
        """

        # Keep the API stable.
        tuple(observations)

        return self.ordered()

    def __contains__(
        self,
        correlator: object,
    ) -> bool:

        return correlator in self._correlators

    def __iter__(self) -> Iterator[Correlation]:

        return iter(self._correlators)

    def __len__(self) -> int:

        return len(self._correlators)

    def __bool__(self) -> bool:

        return bool(self._correlators)

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}"
            f"(correlators={len(self._correlators)})"
        )