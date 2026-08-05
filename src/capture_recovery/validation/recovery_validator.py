from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True, slots=True)
class RecoveryValidationResult:
    """
    Result of recovery validation.
    """

    valid: bool

    score: float

    issues: tuple[str, ...]

    size_match: bool

    content_match: bool

    recovered_size: int

    reference_size: int



class RecoveryValidator:
    """
    Validate recovered binary data.

    Keeps compatibility with the original
    validation API while allowing future
    Capture structural validators.
    """



    def validate(
        self,
        reference: bytes | Path,
        recovered: bytes | Path,
    ) -> RecoveryValidationResult:
        """
        Validate recovered data.
        """

        reference_data = self._read(
            reference,
        )

        recovered_data = self._read(
            recovered,
        )


        size_match = (
            len(reference_data)
            ==
            len(recovered_data)
        )


        score = self._similarity(
            reference_data,
            recovered_data,
        )


        issues: list[str] = []


        if not size_match:

            issues.append(
                "Size mismatch"
            )


        if score < 0.5:

            issues.append(
                "Low binary similarity"
            )


        elif score < 1.0:

            issues.append(
                "Binary difference detected"
            )


        return RecoveryValidationResult(
            valid=(
                score == 1.0
            ),

            score=score,

            issues=tuple(
                issues
            ),

            size_match=size_match,

            content_match=(
                reference_data
                ==
                recovered_data
            ),

            recovered_size=len(
                recovered_data
            ),

            reference_size=len(
                reference_data
            ),
        )



    def validate_file(
        self,
        reference: Path,
        recovered: Path,
    ) -> RecoveryValidationResult:
        """
        Validate two files.
        """

        return self.validate(
            reference,
            recovered,
        )



    @staticmethod
    def _similarity(
        reference: bytes,
        recovered: bytes,
    ) -> float:
        """
        Calculate binary similarity score.
        """

        if (
            not reference
            and
            not recovered
        ):
            return 1.0


        if not reference or not recovered:

            return 0.0


        size = max(
            len(reference),
            len(recovered),
        )


        matches = 0


        for index in range(size):

            ref = (
                reference[index]
                if index < len(reference)
                else None
            )

            rec = (
                recovered[index]
                if index < len(recovered)
                else None
            )


            if ref == rec:

                matches += 1


        return matches / size



    @staticmethod
    def _read(
        value: bytes | Path,
    ) -> bytes:
        """
        Normalize validation input.
        """

        if isinstance(
            value,
            bytes,
        ):

            return value


        if isinstance(
            value,
            Path,
        ):

            return value.read_bytes()


        raise TypeError(
            "Expected bytes or Path"
        )