from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ValidationResult:
    """
    Result of project validation.
    """

    errors: list[str] = field(
        default_factory=list,
    )

    warnings: list[str] = field(
        default_factory=list,
    )

    @property
    def valid(self) -> bool:
        return not self.errors

    def add_error(
        self,
        message: str,
    ) -> None:
        self.errors.append(
            message,
        )

    def add_warning(
        self,
        message: str,
    ) -> None:
        self.warnings.append(
            message,
        )

    def __bool__(self) -> bool:
        return self.valid