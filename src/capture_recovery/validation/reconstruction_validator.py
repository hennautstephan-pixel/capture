from __future__ import annotations

from capture_recovery.models.project import Project

from .project_validator import ProjectValidator
from .validation_result import ValidationResult


class ReconstructionValidator:
    """
    Validate a reconstructed Capture project.

    Entry point after reconstruction.
    """

    def __init__(
        self,
        project_validator: ProjectValidator | None = None,
    ) -> None:

        self._project_validator = (
            project_validator
            or ProjectValidator()
        )


    def validate(
        self,
        project: Project,
    ) -> ValidationResult:
        """
        Validate a reconstructed project.
        """

        return self._project_validator.validate(
            project,
        )