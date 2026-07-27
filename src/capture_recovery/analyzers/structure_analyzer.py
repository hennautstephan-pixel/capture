from __future__ import annotations

from ..models import Block, Report


class StructureAnalyzer:
    """
    Regroupe les détections proches en blocs.

    Cette première implémentation utilise uniquement
    la proximité des offsets.
    """

    def __init__(
        self,
        max_gap: int = 32,
        minimum_detections: int = 2,
    ) -> None:

        self.max_gap = max_gap
        self.minimum_detections = minimum_detections

    def analyze(self, report: Report) -> None:
        """
        Construit des blocs à partir des détections.
        """

        if not report.detections:
            return

        detections = sorted(
            report.detections,
            key=lambda d: d.offset,
        )

        current = [detections[0]]

        for detection in detections[1:]:

            previous = current[-1]

            gap = detection.offset - previous.end

            if gap <= self.max_gap:
                current.append(detection)
                continue

            self._create_block(current, report)

            current = [detection]

        self._create_block(current, report)

    def _create_block(
        self,
        detections,
        report: Report,
    ) -> None:

        if len(detections) < self.minimum_detections:
            return

        start = detections[0].offset
        end = detections[-1].end

        datatypes = {
            detection.datatype
            for detection in detections
        }

        if len(datatypes) == 1:
            name = next(iter(datatypes)).upper()
        else:
            name = "MIXED"

        block = Block(
            name=name,
            offset=start,
            length=end - start,
            metadata={
                "detections": len(detections),
                "types": sorted(datatypes),
            },
        )

        report.add_block(block)