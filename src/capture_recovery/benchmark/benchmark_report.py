"""
Benchmark report.
"""

from __future__ import annotations

import json

from .benchmark_statistics import BenchmarkStatistics


class BenchmarkReport:
    """
    Generates reports from benchmark statistics.
    """

    def __init__(
        self,
        statistics: BenchmarkStatistics,
    ) -> None:

        self._statistics = statistics

    @property
    def statistics(self) -> BenchmarkStatistics:
        return self._statistics

    def to_text(self) -> str:
        """
        Generate a plain text report.
        """

        s = self._statistics

        return "\n".join(
            [
                "Capture Recovery Benchmark",
                "=" * 28,
                "",
                f"Projects analysed   : {s.project_count}",
                f"Objects             : {s.total_objects}",
                f"Recovered           : {s.recovered_objects}",
                f"Recovery            : {s.recovery_rate:.2%}",
                f"Properties          : {s.total_properties}",
                f"Candidates          : {s.total_candidates}",
                f"Confidence          : {s.average_confidence:.3f}",
                f"Conflicts           : {s.total_conflicts}",
                f"Unknown signatures  : {s.total_unknown_signatures}",
                f"Duration            : {s.total_duration:.2f} s",
            ]
        )

    def to_markdown(self) -> str:
        """
        Generate a Markdown report.
        """

        s = self._statistics

        return "\n".join(
            [
                "# Capture Recovery Benchmark",
                "",
                "| Metric | Value |",
                "|--------|------:|",
                f"| Projects | {s.project_count} |",
                f"| Objects | {s.total_objects} |",
                f"| Recovered | {s.recovered_objects} |",
                f"| Recovery | {s.recovery_rate:.2%} |",
                f"| Properties | {s.total_properties} |",
                f"| Candidates | {s.total_candidates} |",
                f"| Average confidence | {s.average_confidence:.3f} |",
                f"| Conflicts | {s.total_conflicts} |",
                f"| Unknown signatures | {s.total_unknown_signatures} |",
                f"| Duration | {s.total_duration:.2f} s |",
            ]
        )

    def to_json(self) -> str:
        """
        Generate a JSON report.
        """

        return json.dumps(
            self._statistics.to_dict(),
            indent=4,
            sort_keys=True,
        )

    def __str__(self) -> str:
        return self.to_text()