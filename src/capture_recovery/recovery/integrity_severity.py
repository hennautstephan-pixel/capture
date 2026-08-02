from __future__ import annotations

from enum import Enum


class IntegritySeverity(str, Enum):
    """
    Severity of an integrity issue detected during project recovery.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    @property
    def is_fatal(self) -> bool:
        """
        Returns True if the issue is considered fatal for opening
        a Capture project.
        """
        return self is IntegritySeverity.CRITICAL

    @property
    def is_error(self) -> bool:
        """
        Returns True if the issue represents an error.
        """
        return self in (
            IntegritySeverity.ERROR,
            IntegritySeverity.CRITICAL,
        )