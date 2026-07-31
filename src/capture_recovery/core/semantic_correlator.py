from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class SemanticObject:
    """Represents a business object reconstructed from several detected values.

    The instance is intentionally immutable so that correlation results can be
    safely reused and compared without accidental mutation.
    """

    object_type: str
    """The semantic category or type assigned to this reconstructed object."""

    properties: dict[str, Any]
    """A dictionary of extracted or inferred properties attached to the object."""

    confidence: float
    """A confidence score indicating how strongly the object is supported."""

    source_offsets: tuple[int, ...]
    """The source offsets that contributed to the reconstruction of this object."""


class SemanticCorrelator(ABC):
    """Abstract base class for future semantic correlation engines.

    This foundation is intentionally generic so that specialized correlators can
    be introduced later without changing the surrounding architecture. Planned
    extensions include FixtureCorrelator, SceneCorrelator, DMXCorrelator, and
    GroupCorrelator.
    """

    @abstractmethod
    def correlate(self, values: Iterable[Any]) -> list[SemanticObject]:
        """Return semantic objects reconstructed from the provided values.

        The current implementation is intentionally empty and only establishes the
        public interface expected by future specialized correlators.
        """
        return []


__all__ = ["SemanticObject", "SemanticCorrelator"]
