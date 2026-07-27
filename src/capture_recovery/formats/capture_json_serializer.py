"""
Capture project JSON serializer.

Converts a CaptureProject model into
a JSON-compatible representation.
"""

from __future__ import annotations

import json
from pathlib import Path

from .capture_project import CaptureProject


class CaptureJsonSerializer:
    """
    Serialize CaptureProject objects to JSON.
    """

    def to_dict(
        self,
        project: CaptureProject,
    ) -> dict:
        """
        Convert CaptureProject into a dictionary.
        """

        return {
            "project": {
                "name": project.name,
                "metadata": project.metadata,
            },
            "fixtures": [
                {
                    "name": fixture.name,
                    "universe": fixture.universe,
                    "address": fixture.address,
                    "manufacturer": fixture.manufacturer,
                    "model": fixture.model,
                    "mode": fixture.mode,
                    "properties": fixture.properties,
                }
                for fixture in project.fixtures
            ],
            "universes": [
                {
                    "name": universe.name,
                    "universe": universe.universe,
                    "protocol": universe.protocol,
                    "properties": universe.properties,
                }
                for universe in project.universes
            ],
            "cues": [
                {
                    "name": cue.name,
                    "number": cue.number,
                    "properties": cue.properties,
                }
                for cue in project.cues
            ],
        }

    def to_string(
        self,
        project: CaptureProject,
    ) -> str:
        """
        Return formatted JSON text.
        """

        return json.dumps(
            self.to_dict(project),
            indent=4,
            ensure_ascii=False,
        )

    def save(
        self,
        project: CaptureProject,
        path: str | Path,
    ) -> None:
        """
        Save Capture project JSON.
        """

        path = Path(path)

        path.write_text(
            self.to_string(project),
            encoding="utf-8",
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}()"
        )