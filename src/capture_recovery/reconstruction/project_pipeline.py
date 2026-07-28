"""
Reconstruction pipeline.

Runs final reconstruction checks
before export.
"""

from __future__ import annotations

from capture_recovery.validation import (
    ReconstructionValidator,
)


class ReconstructionPipeline:
    """
    Complete reconstruction workflow.
    """

    def __init__(
        self,
        validator=None,
    ) -> None:

        self.validator = (
            validator
            or ReconstructionValidator()
        )


    def process(
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

            "project": project,

        }