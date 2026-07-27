from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path

from ..models import Report


class JsonExporter:
    """Exporte un Report au format JSON."""

    def export(
        self,
        report: Report,
        filename: str | Path,
    ) -> None:

        path = Path(filename)

        if not is_dataclass(report):
            raise TypeError("report must be a dataclass")

        data = asdict(report)

        path.write_text(
            json.dumps(
                data,
                indent=4,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )