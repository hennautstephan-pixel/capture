from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DiffReport:
    """
    Résultat de la comparaison entre deux rapports.
    """

    filename_a: str
    filename_b: str

    statistics: dict[str, tuple[int, int]] = field(default_factory=dict)

    added_detections: int = 0
    removed_detections: int = 0

    added_blocks: int = 0
    removed_blocks: int = 0

    hypotheses: list[str] = field(default_factory=list)