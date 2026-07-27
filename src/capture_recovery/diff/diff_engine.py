from __future__ import annotations

from .diff_report import DiffReport
from .statistics_diff import StatisticsDiff


class DiffEngine:

    def compare(
        self,
        report_a,
        report_b,
    ) -> DiffReport:

        report = DiffReport(
            filename_a=report_a.filename,
            filename_b=report_b.filename,
        )

        report.statistics = StatisticsDiff().compare(
            report_a,
            report_b,
        )

        report.added_detections = max(
            0,
            report_b.detection_count - report_a.detection_count,
        )

        report.removed_detections = max(
            0,
            report_a.detection_count - report_b.detection_count,
        )

        report.added_blocks = max(
            0,
            report_b.block_count - report_a.block_count,
        )

        report.removed_blocks = max(
            0,
            report_a.block_count - report_b.block_count,
        )

        return report