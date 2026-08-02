from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from .project_layout import (
    LayoutRegion,
    ProjectLayout,
)


class IntegritySeverity(Enum):
    """
    Severity of an integrity issue.
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()


@dataclass(slots=True, frozen=True)
class IntegrityIssue:
    """
    One detected integrity issue.
    """

    severity: IntegritySeverity

    message: str

    region: LayoutRegion | None = None


@dataclass(slots=True, frozen=True)
class IntegrityReport:
    """
    Result of a project integrity analysis.
    """

    issues: list[IntegrityIssue]

    score: float

    @property
    def valid(self) -> bool:
        return self.error_count == 0

    @property
    def error_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.ERROR
            for issue in self.issues
        )

    @property
    def warning_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.WARNING
            for issue in self.issues
        )

    @property
    def info_count(self) -> int:
        return sum(
            issue.severity is IntegritySeverity.INFO
            for issue in self.issues
        )

    @property
    def critical(self) -> bool:
        """
        True when at least one structural error
        has been detected.
        """
        return self.error_count > 0

    @property
    def recoverable(self) -> bool:
        """
        Simple heuristic used by future repair
        strategies.
        """
        return self.score >= 0.50

    def by_severity(self) -> list[IntegrityIssue]:
        """
        Return issues ordered by severity.
        """

        priority = {
            IntegritySeverity.ERROR: 0,
            IntegritySeverity.WARNING: 1,
            IntegritySeverity.INFO: 2,
        }

        return sorted(
            self.issues,
            key=lambda issue: (
                priority[issue.severity],
                issue.message,
            ),
        )


class IntegrityAnalyzer:
    """
    Validate the physical consistency of a project layout.

    This class validates only structural integrity.
    It does not attempt to understand Capture semantics.
    """

    def analyze(
        self,
        layout: ProjectLayout,
    ) -> IntegrityReport:

        issues: list[IntegrityIssue] = []

        self._check_region(
            layout.header,
            "Header",
            issues,
        )

        self._check_region(
            layout.stream,
            "Stream",
            issues,
        )

        self._check_region(
            layout.footer,
            "Footer",
            issues,
        )

        self._check_objects(
            layout,
            issues,
        )

        self._check_gaps(
            layout,
            issues,
        )

        errors = sum(
            issue.severity is IntegritySeverity.ERROR
            for issue in issues
        )

        warnings = sum(
            issue.severity is IntegritySeverity.WARNING
            for issue in issues
        )

        score = max(
            0.0,
            1.0
            - errors * 0.20
            - warnings * 0.05,
        )

        return IntegrityReport(
            issues=issues,
            score=score,
        )

    @staticmethod
    def _check_region(
        region: LayoutRegion,
        name: str,
        issues: list[IntegrityIssue],
    ) -> None:

        if region.length <= 0:

            issues.append(
                IntegrityIssue(
                    IntegritySeverity.ERROR,
                    f"{name} has zero length.",
                    region,
                )
            )

    @staticmethod
    def _check_objects(
        layout: ProjectLayout,
        issues: list[IntegrityIssue],
    ) -> None:

        stream = layout.stream

        previous_end = stream.offset

        for obj in layout.objects:

            if obj.offset < stream.offset:

                issues.append(
                    IntegrityIssue(
                        IntegritySeverity.ERROR,
                        "Object starts before stream.",
                    )
                )

            if obj.end > stream.end:

                issues.append(
                    IntegrityIssue(
                        IntegritySeverity.ERROR,
                        "Object exceeds stream.",
                    )
                )

            if obj.offset < previous_end:

                issues.append(
                    IntegrityIssue(
                        IntegritySeverity.WARNING,
                        "Objects overlap.",
                    )
                )

            previous_end = max(
                previous_end,
                obj.end,
            )

    @staticmethod
    def _check_gaps(
        layout: ProjectLayout,
        issues: list[IntegrityIssue],
    ) -> None:

        for gap in layout.gaps:

            if gap.length <= 0:

                issues.append(
                    IntegrityIssue(
                        IntegritySeverity.WARNING,
                        "Empty gap.",
                        gap,
                    )
                )