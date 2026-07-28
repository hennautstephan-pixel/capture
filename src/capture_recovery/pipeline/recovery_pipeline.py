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
        reader=None,
        validator=None,
        finalizer=None,
    ) -> None:

        self.reader = (
            reader
            or CaptureReader()
        )

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
        path,
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

        errors = self.validator.validate(
            project,
        )

        return {

            "valid": len(errors) == 0,

            "errors": errors,

        }


    def finalize(
        self,
        project,
    ):
        """
        Finalize project.
        """

        return self.finalizer.finalize(
            project,
        )


    def run(
        self,
        path,
        project,
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