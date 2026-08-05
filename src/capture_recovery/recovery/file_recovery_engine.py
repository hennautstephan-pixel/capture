from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.reconstruction.recovery_orchestrator import (
    RecoveryOrchestrator,
    RecoveryResult,
)


from capture_recovery.validation.recovery_validator import (
    RecoveryValidator,
    RecoveryValidationResult,
)



@dataclass(frozen=True, slots=True)
class FileRecoveryResult:
    """
    Result of a file recovery operation.
    """

    success: bool

    input_file: Path

    reference_file: Path

    output_file: Path

    input_size: int

    output_size: int

    repaired_regions: int

    recovery: RecoveryResult

    validation: RecoveryValidationResult



class FileRecoveryEngine:
    """
    High level file recovery service.

    Reads files, runs reconstruction,
    writes output and validates result.
    """



    def __init__(
        self,
        orchestrator: RecoveryOrchestrator,
        validator: RecoveryValidator | None = None,
    ) -> None:

        self._orchestrator = orchestrator


        self._validator = (
            validator
            if validator is not None
            else RecoveryValidator()
        )



    def recover_file(
        self,
        source: Path,
        reference: Path,
        output: Path,
        *,
        object_type: str,
    ) -> FileRecoveryResult:
        """
        Recover a Capture project file.
        """

        if not source.exists():

            raise FileNotFoundError(
                source
            )


        if not reference.exists():

            raise FileNotFoundError(
                reference
            )


        damaged = source.read_bytes()

        reference_data = reference.read_bytes()


        recovery = self._orchestrator.recover(
            damaged,

            reference_data,

            object_type=object_type,
        )


        output.write_bytes(
            recovery.data
        )


        validation = self._validator.validate(
            reference_data,

            recovery.data,
        )


        return FileRecoveryResult(
            success=(
                recovery.success
                and
                validation.valid
            ),

            input_file=source,

            reference_file=reference,

            output_file=output,

            input_size=len(damaged),

            output_size=len(recovery.data),

            repaired_regions=len(
                recovery.decisions
            ),

            recovery=recovery,

            validation=validation,
        )