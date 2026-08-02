"""
Reconstruction candidate.

A reconstruction candidate represents one possible repair of a damaged binary
structure. Candidates are produced by heuristics and later ranked by the
reconstruction registry.

The class is immutable so that candidates can safely be cached, compared and
shared between heuristics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True, order=True)
class ReconstructionCandidate:
    """
    A possible reconstruction of a damaged structure.

    Parameters
    ----------
    score:
        Confidence score in the range [0.0, 1.0].

    heuristic:
        Name of the heuristic that produced this candidate.

    description:
        Human-readable explanation.

    modifications:
        Dictionary describing the proposed modifications.

    metadata:
        Optional diagnostic information.
    """

    score: float
    heuristic: str
    description: str = ""

    modifications: Mapping[str, Any] = field(default_factory=dict, compare=False)
    metadata: Mapping[str, Any] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0.0 and 1.0")

    @property
    def confidence(self) -> float:
        """Alias for score."""
        return self.score

    @property
    def modification_count(self) -> int:
        """Return the number of proposed modifications."""
        return len(self.modifications)

    @property
    def is_empty(self) -> bool:
        """True if the candidate proposes no modification."""
        return self.modification_count == 0

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """Retrieve a proposed modification."""
        return self.modifications.get(key, default)

    def explain(self) -> str:
        """
        Return a human-readable explanation.

        Example
        -------
        OffsetRecovery (94.2%) : recovered block length
        """

        percentage = self.score * 100.0

        if self.description:
            return (
                f"{self.heuristic} "
                f"({percentage:.1f}%) : "
                f"{self.description}"
            )

        return f"{self.heuristic} ({percentage:.1f}%)"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the candidate to a serialisable dictionary.
        """

        return {
            "heuristic": self.heuristic,
            "score": self.score,
            "description": self.description,
            "modifications": dict(self.modifications),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def empty(
        cls,
        heuristic: str = "Unknown",
    ) -> "ReconstructionCandidate":
        """
        Create an empty candidate.

        Useful for placeholder heuristics and testing.
        """

        return cls(
            score=0.0,
            heuristic=heuristic,
            description="No reconstruction proposed",
        )