from __future__ import annotations

from pathlib import Path

from ..binary_reader import BinaryReader
from ..detectors.pipeline import DetectorPipeline
from ..models import Report


class FileScanner:

    def __init__(
        self,
        pipeline: DetectorPipeline,
    ):
        self.pipeline = pipeline

    def scan(
        self,
        filename: str | Path,
    ) -> Report:

        with BinaryReader(filename) as reader:

            data = reader.read_safe(reader.size)

            report = Report(
                filename=str(filename),
                filesize=reader.size,
            )

            report.detections = self.pipeline.detect(data)

            return report