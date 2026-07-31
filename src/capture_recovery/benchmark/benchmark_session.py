"""
Benchmark session.
"""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .benchmark_statistics import BenchmarkStatistics


@dataclass(slots=True)
class BenchmarkSession:
    """
    Represents a complete benchmark execution.
    """

    samples_directory: Path

    statistics: BenchmarkStatistics = field(
        default_factory=BenchmarkStatistics
    )

    started_at: datetime = field(
        default_factory=datetime.now
    )

    finished_at: datetime | None = None

    framework_version: str = "development"

    python_version: str = field(
        default_factory=lambda: (
            f"{sys.version_info.major}."
            f"{sys.version_info.minor}."
            f"{sys.version_info.micro}"
        )
    )

    platform: str = field(
        default_factory=platform.platform
    )

    def finish(self) -> None:
        """
        Mark the session as finished.
        """

        self.finished_at = datetime.now()

    @property
    def duration_seconds(self) -> float:
        """
        Returns the execution duration.
        """

        if self.finished_at is None:
            return 0.0

        return (
            self.finished_at - self.started_at
        ).total_seconds()

    @property
    def completed(self) -> bool:
        """
        Indicates whether the benchmark has completed.
        """

        return self.finished_at is not None

    def to_dict(self) -> dict[str, object]:
        """
        Serialize the benchmark session.
        """

        return {
            "samples_directory": str(
                self.samples_directory
            ),
            "started_at": self.started_at.isoformat(),
            "finished_at": (
                self.finished_at.isoformat()
                if self.finished_at
                else None
            ),
            "duration_seconds": self.duration_seconds,
            "framework_version": self.framework_version,
            "python_version": self.python_version,
            "platform": self.platform,
            "statistics": self.statistics.to_dict(),
        }