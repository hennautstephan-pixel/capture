from __future__ import annotations

from dataclasses import dataclass, field

from .block import Block
from .detection import Detection
from .finding import Finding
from .statistics import Statistics


@dataclass(slots=True)
class Report:
    """Rapport complet produit par l'analyse d'un fichier."""

    filename: str
    filesize: int

    detections: list[Detection] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    blocks: list[Block] = field(default_factory=list)

    statistics: Statistics = field(default_factory=Statistics)

    def add_detection(self, detection: Detection) -> None:
        self.detections.append(detection)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)

    def add_block(self, block: Block) -> None:
        self.blocks.append(block)

    def update_statistics(self) -> None:
        """Recalcule automatiquement les statistiques."""

        stats = Statistics()

        for detection in self.detections:

            match detection.datatype:

                case "ascii":
                    stats.ascii_strings += 1

                case "utf16":
                    stats.utf16_strings += 1

                case "int32" | "uint32":
                    stats.integers += 1

                case "float":
                    stats.floats += 1

                case _:
                    if detection.datatype.startswith("zip"):
                        stats.signatures += 1
                    elif detection.datatype.startswith("png"):
                        stats.signatures += 1
                    elif detection.datatype.startswith("jpeg"):
                        stats.signatures += 1
                    elif detection.datatype.startswith("gif"):
                        stats.signatures += 1
                    elif detection.datatype.startswith("xml"):
                        stats.signatures += 1

        stats.blocks = len(self.blocks)

        self.statistics = stats

    @property
    def detection_count(self) -> int:
        return len(self.detections)

    @property
    def block_count(self) -> int:
        return len(self.blocks)

    @property
    def finding_count(self) -> int:
        return len(self.findings)

    def summary(self) -> str:
        """Résumé lisible du rapport."""

        self.update_statistics()

        return (
            f"File: {self.filename}\n"
            f"Size: {self.filesize:,} bytes\n"
            f"Detections: {self.detection_count}\n"
            f"Blocks: {self.block_count}\n"
            f"Findings: {self.finding_count}"
        )