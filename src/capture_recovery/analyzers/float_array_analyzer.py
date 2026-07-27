from __future__ import annotations

from ..models import Block, Report


class FloatArrayAnalyzer:
    """
    Détecte les longues séquences de floats contigus.
    """

    def __init__(
        self,
        minimum_count: int = 16,
        max_gap: int = 4,
    ) -> None:

        self.minimum_count = minimum_count
        self.max_gap = max_gap

    def analyze(
        self,
        report: Report,
    ) -> None:

        floats = sorted(
            (
                detection
                for detection in report.detections
                if detection.datatype == "float"
            ),
            key=lambda d: d.offset,
        )

        if not floats:
            return

        current = [floats[0]]

        for detection in floats[1:]:

            previous = current[-1]

            gap = detection.offset - previous.end

            #
            # Deux floats sont censés être espacés de 4 octets.
            #

            if gap <= self.max_gap:

                current.append(detection)

                continue

            self._flush(
                current,
                report,
            )

            current = [detection]

        self._flush(
            current,
            report,
        )

    def _flush(
        self,
        floats,
        report: Report,
    ) -> None:

        if len(floats) < self.minimum_count:
            return

        start = floats[0].offset
        end = floats[-1].end

        report.add_block(

            Block(
                name="FLOAT_ARRAY",
                offset=start,
                length=end - start,
                metadata={
                    "count": len(floats),
                    "bytes": end - start,
                },
            )

        )