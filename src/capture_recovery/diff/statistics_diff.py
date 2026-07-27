from __future__ import annotations

from ..models import Report


class StatisticsDiff:

    FIELDS = (
        "ascii_strings",
        "utf16_strings",
        "integers",
        "floats",
        "signatures",
        "blocks",
    )

    def compare(
        self,
        report_a: Report,
        report_b: Report,
    ) -> dict[str, tuple[int, int]]:

        result = {}

        for field in self.FIELDS:

            result[field] = (
                getattr(report_a.statistics, field),
                getattr(report_b.statistics, field),
            )

        return result