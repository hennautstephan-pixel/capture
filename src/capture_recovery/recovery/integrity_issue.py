from __future__ import annotations

from dataclasses import dataclass

from .integrity_severity import IntegritySeverity


@dataclass(slots=True)
class IntegrityIssue:
    """
    Represents a single integrity problem detected while analysing
    a Capture project.
    """

    code: str
    message: str
    severity: IntegritySeverity
    location: str | None = None
    recoverable: bool = True
    recommendation: str | None = None

    @property
    def fatal(self) -> bool:
        return (
            self.severity.is_fatal
            and not self.recoverable
        )

    def __str__(self) -> str:

        if self.location:
            return (
                f"[{self.severity.value.upper()}] "
                f"{self.location}: "
                f"{self.message}"
            )

        return (
            f"[{self.severity.value.upper()}] "
            f"{self.message}"
        )