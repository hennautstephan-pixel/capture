"""
Capture project recovery pipeline.

Loads Capture project files (.c2p)
and prepares them for reconstruction.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.formats import (
    CaptureProjectReader,
)


class CaptureProjectPipeline:
    """
    Pipeline dedicated to Capture project files.
    """


    def __init__(
        self,
        reader: CaptureProjectReader | None = None,
    ):

        self.reader = (
            reader
            if reader is not None
            else CaptureProjectReader()
        )


    def process(
        self,
        path,
    ) -> dict:
        """
        Process a Capture project.

        Returns normalized recovery data.
        """

        path = Path(path)


        project = self.reader.read(
            path
        )


        return {

            "success": True,

            "source": str(path),

            "project": project,

            "fixtures": project.get(
                "fixtures",
                [],
            ),

            "scenes": project.get(
                "scenes",
                [],
            ),

            "patch": project.get(
                "patch",
                [],
            ),

            "metadata": project.get(
                "metadata",
                {},
            ),
        }