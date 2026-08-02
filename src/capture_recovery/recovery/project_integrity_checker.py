from __future__ import annotations

from capture_recovery.recovery import IntegrityReport


class ProjectIntegrityChecker:

    def __init__(
        self,
        checks=None,
    ) -> None:

        self._checks = list(checks or [])

    def add_check(
        self,
        check,
    ) -> None:

        self._checks.append(check)

    def check(
        self,
        project,
    ) -> IntegrityReport:

        report = IntegrityReport()

        for check in self._checks:
            check.check(
                project,
                report,
            )

        return report