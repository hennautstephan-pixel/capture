from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from .hypothesis import Hypothesis


@dataclass(slots=True)
class HypothesisResult:
    """
    Collection of semantic hypotheses.

    The hypotheses are automatically kept sorted by decreasing
    confidence.
    """

    hypotheses: list[Hypothesis] = field(
        default_factory=list,
    )

    metadata: dict = field(
        default_factory=dict,
    )

    def __post_init__(self) -> None:

        self.hypotheses.sort(
            key=lambda h: h.confidence,
            reverse=True,
        )

    @property
    def empty(self) -> bool:

        return not self.hypotheses

    @property
    def count(self) -> int:

        return len(self.hypotheses)

    @property
    def confidence(self) -> float:

        if self.empty:
            return 0.0

        return self.hypotheses[0].confidence

    def best(self) -> Hypothesis | None:

        if self.empty:
            return None

        return self.hypotheses[0]

    def top(
        self,
        n: int = 5,
    ) -> list[Hypothesis]:

        return self.hypotheses[:n]

    def by_type(
        self,
        object_type: str,
    ) -> list[Hypothesis]:

        return [
            h
            for h in self.hypotheses
            if h.object_type == object_type
        ]

    def above(
        self,
        confidence: float,
    ) -> list[Hypothesis]:

        return [
            h
            for h in self.hypotheses
            if h.confidence >= confidence
        ]

    def add(
        self,
        hypothesis: Hypothesis,
    ) -> None:

        self.hypotheses.append(
            hypothesis,
        )

        self.hypotheses.sort(
            key=lambda h: h.confidence,
            reverse=True,
        )

    def extend(
        self,
        hypotheses,
    ) -> None:

        self.hypotheses.extend(
            hypotheses,
        )

        self.hypotheses.sort(
            key=lambda h: h.confidence,
            reverse=True,
        )

    def clear(self) -> None:

        self.hypotheses.clear()

    def __len__(self) -> int:

        return len(self.hypotheses)

    def __iter__(
        self,
    ) -> Iterator[Hypothesis]:

        return iter(self.hypotheses)

    def __getitem__(
        self,
        index: int,
    ) -> Hypothesis:

        return self.hypotheses[index]

    def __contains__(
        self,
        hypothesis: Hypothesis,
    ) -> bool:

        return hypothesis in self.hypotheses

    def __repr__(self) -> str:

        return (
            "HypothesisResult("
            f"{len(self)} hypotheses)"
        )