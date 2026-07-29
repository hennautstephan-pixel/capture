"""
Project exporter.

Serialize recovered Capture projects.
"""

from __future__ import annotations

from pathlib import Path

from .capture_project_writer import (
    CaptureProjectWriter,
)



class ProjectExporter:
    """
    Wrapper around CaptureProjectWriter.
    """



    def __init__(
        self,
    ) -> None:

        self.writer = (
            CaptureProjectWriter()
        )



    def export(
        self,
        project,
        filename,
    ) -> Path:
        """
        Export CaptureProject.
        """

        path = Path(
            filename
        )


        self.writer.write(
            project,
            path,
        )


        return path