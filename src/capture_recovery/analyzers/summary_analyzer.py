from collections import Counter

from ..models import Report


class SummaryAnalyzer:
    """Produit un résumé statistique des détections."""

    def analyze(self, report: Report) -> None:

        counts = Counter(
            detection.datatype
            for detection in report.detections
        )

        report.statistics.by_type = dict(counts)