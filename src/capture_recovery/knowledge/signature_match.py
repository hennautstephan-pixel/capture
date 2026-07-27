from __future__ import annotations

from dataclasses import dataclass, field

from .signature import Signature


@dataclass(slots=True, frozen=True)
class SignatureMatch:
    """
    Result of matching a Structure against a Signature.
    """

    signature: Signature

    score: int

    matched_required: tuple[str, ...] = field(default_factory=tuple)

    matched_optional: tuple[str, ...] = field(default_factory=tuple)

    missing_required: tuple[str, ...] = field(default_factory=tuple)

    confidence: float = 1.0

    @property
    def accepted(self) -> bool:
        """
        Return True if the signature score reaches the acceptance threshold.
        """
        return self.score >= self.signature.minimum_score

    @property
    def maximum_score(self) -> int:
        """
        Maximum score of the signature.
        """
        return self.signature.maximum_score

    @property
    def percentage(self) -> float:
        """
        Return the normalized score between 0 and 100.
        """
        if self.maximum_score == 0:
            return 0.0

        return (self.score / self.maximum_score) * 100.0

    @property
    def matched_fields(self) -> tuple[str, ...]:
        """
        Return every matched field.
        """
        return (
            self.matched_required
            + self.matched_optional
        )

    @property
    def missing_count(self) -> int:
        return len(self.missing_required)

    @property
    def matched_count(self) -> int:
        return len(self.matched_fields)

    def has_missing(self) -> bool:
        return bool(self.missing_required)

    def is_perfect(self) -> bool:
        """
        Perfect match:
            - accepted
            - no required field missing
            - full score
        """
        return (
            self.accepted
            and not self.missing_required
            and self.score == self.maximum_score
        )

    def __len__(self) -> int:
        return self.matched_count

    def __bool__(self) -> bool:
        return self.accepted

    def __str__(self) -> str:
        return (
            f"{self.signature.name}"
            f" ({self.score}/{self.maximum_score}"
            f" = {self.percentage:.1f}%)"
        )