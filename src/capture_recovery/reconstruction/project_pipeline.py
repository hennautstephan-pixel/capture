"""
Reconstruction pipeline.

Runs final reconstruction checks
before export.
"""

from __future__ import annotations

from capture_recovery.validation import ReconstructionValidator


class ReconstructionPipeline:
    """
    Complete reconstruction workflow.
    """

    def __init__(
        self,
        validator: ReconstructionValidator | None = None,
    ) -> None:
        self.validator = validator or ReconstructionValidator()

    def process(
        self,
        project,
    ) -> dict:
        """
        Validate reconstructed project.
        """

        validation = self.validator.validate(project)

        return {
            "valid": validation.valid,
            "errors": list(validation.errors),
            "warnings": list(validation.warnings),
            "project": project,
        }