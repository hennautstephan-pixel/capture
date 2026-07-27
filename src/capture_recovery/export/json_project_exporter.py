"""
JSON exporter for reconstructed Capture projects.
"""

from __future__ import annotations

import json
from pathlib import Path

from capture_recovery.models.project import Project


class JsonProjectExporter:
    """
    Export a reconstructed project to JSON.
    """

    def export_dict(
        self,
        project: Project,
    ) -> dict:
        """
        Convert a project into a JSON-compatible dictionary.
        """

        return {
            "name": project.name,
            "objects": [
                {
                    "type": obj.object_type,
                    "identifier": obj.identifier,
                    "properties": obj.properties,
                    "confidence": obj.confidence,
                }
                for obj in project
            ],
        }

    def export_string(
        self,
        project: Project,
    ) -> str:
        """
        Return formatted JSON string.
        """

        return json.dumps(
            self.export_dict(project),
            indent=4,
            ensure_ascii=False,
        )

    def export_file(
        self,
        project: Project,
        path: str | Path,
    ) -> None:
        """
        Write project JSON to disk.
        """

        path = Path(path)

        path.write_text(
            self.export_string(project),
            encoding="utf-8",
        )