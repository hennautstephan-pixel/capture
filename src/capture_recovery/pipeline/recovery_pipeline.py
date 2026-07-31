"""
Recovery pipeline.

Coordinates the complete Capture recovery workflow.
"""

from __future__ import annotations

from capture_recovery.io import (
    CaptureReader,
)
from capture_recovery.reconstruction import (
    ProjectFinalize,
)
from capture_recovery.validation import (
    ReconstructionValidator,
)


class RecoveryPipeline:
    """
    Main recovery workflow.
    """

    def __init__(
        self,
        reader: CaptureReader | None = None,
        validator: ReconstructionValidator | None = None,
        finalizer: ProjectFinalize | None = None,
    ) -> None:
        self.reader = reader or CaptureReader()

        self.validator = (
            validator
            or ReconstructionValidator()
        )

        self.finalizer = (
            finalizer
            or ProjectFinalize()
        )

    def load(
        self,
        path: str,
    ) -> dict:
        """
        Load Capture data.
        """

        return self.reader.read(
            path,
        )

    def validate(
        self,
        project,
    ) -> dict:
        """
        Validate reconstructed project.
        """

        result = self.validator.validate(project)

        return {
            "valid": result.valid,
            "errors": list(result.errors),
            "warnings": list(result.warnings),
        }

    def finalize(
        self,
        project: dict,
    ) -> dict:
        """
        Finalize project.
        """

        return self.finalizer.finalize(
            project,
        )

    def run(
        self,
        path: str,
        project: dict,
    ) -> dict:
        """
        Execute recovery workflow.
        """

        source = self.load(
            path,
        )

        result = self.validate(
            project,
        )

        if result["valid"]:
            project = self.finalize(
                project,
            )

        return {
            "source": source,
            "validation": result,
            "project": project,
        }