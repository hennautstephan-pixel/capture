from __future__ import annotations

from dataclasses import dataclass, field

from .integrity_issue import IntegrityIssue
from .integrity_severity import IntegritySeverity


@dataclass(slots=True)
class IntegrityReport:
    """
    Result of a project integrity analysis.

    This report aggregates every issue detected while analysing a
    Capture project and provides convenient statistics for the
    recovery engine.
    """

    issues: list[IntegrityIssue] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Manipulation
    # ------------------------------------------------------------------

    def add(
        self,
        issue: IntegrityIssue,
    ) -> None:
        """
        Add a new integrity issue.
        """
        self.issues.append(issue)

    def extend(
        self,
        issues: list[IntegrityIssue],
    ) -> None:
        """
        Add several integrity issues.
        """
        self.issues.extend(issues)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    @property
    def count(self) -> int:
        return len(self.issues)

    @property
    def info_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.INFO
            for issue in self.issues
        )

    @property
    def warning_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.WARNING
            for issue in self.issues
        )

    @property
    def error_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.ERROR
            for issue in self.issues
        )

    @property
    def critical_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.CRITICAL
            for issue in self.issues
        )

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    @property
    def has_issues(self) -> bool:
        return bool(self.issues)

    @property
    def has_errors(self) -> bool:
        return (
            self.error_count > 0
            or self.critical_count > 0
        )

    @property
    def has_critical_errors(self) -> bool:
        return self.critical_count > 0

    @property
    def recoverable(self) -> bool:
        """
        Returns True if no unrecoverable issue has been detected.
        """

        return not any(
            issue.fatal
            for issue in self.issues
        )

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def by_severity(
        self,
        severity: IntegritySeverity,
    ) -> list[IntegrityIssue]:

        return [
            issue
            for issue in self.issues
            if issue.severity is severity
        ]

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def summary(self) -> str:

        return (
            f"{self.count} issues "
            f"({self.info_count} info, "
            f"{self.warning_count} warnings, "
            f"{self.error_count} errors, "
            f"{self.critical_count} critical)"
        )

    def to_dict(self) -> dict:

        return {
            "recoverable": self.recoverable,
            "count": self.count,
            "info": self.info_count,
            "warnings": self.warning_count,
            "errors": self.error_count,
            "critical": self.critical_count,
        }