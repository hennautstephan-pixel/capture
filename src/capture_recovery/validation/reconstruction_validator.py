from __future__ import annotations

from capture_recovery.models.project import Project

from .project_validator import ProjectValidator
from .validation_result import ValidationResult


class ReconstructionValidator:
    """
    Validate a reconstructed Capture project.

    This validator is the public entry point used once a project has been
    reconstructed. It currently delegates the validation to ProjectValidator
    and intentionally contains no additional business logic.

    Future versions may orchestrate additional validation stages while
    preserving this stable API.
    """

    def __init__(
        self,
        project_validator: ProjectValidator | None = None,
    ) -> None:
        self._project_validator = project_validator or ProjectValidator()

    def validate(
        self,
        project: Project,
    ) -> ValidationResult:
        """
        Validate a reconstructed project.

        Parameters
        ----------
        project:
            Reconstructed project.

        Returns
        -------
        ValidationResult
            Immutable validation result.
        """
        return self._project_validator.validate(project)