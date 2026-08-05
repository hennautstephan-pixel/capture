from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.formats.capture.header import (
    CaptureHeader,
)


from capture_recovery.formats.capture.header_parser import (
    CaptureHeaderParser,
)


@dataclass(frozen=True, slots=True)
class CaptureHeaderValidationResult:
    """
    Result of Capture header validation.
    """

    valid: bool

    header_found: bool

    issues: tuple[str, ...]

    header: CaptureHeader | None = None



class CaptureHeaderValidator:
    """
    Validate Capture project file headers.

    Checks:
        - header presence
        - parser compatibility
        - basic header consistency
    """



    def __init__(
        self,
        parser: CaptureHeaderParser | None = None,
    ) -> None:

        self._parser = (
            parser
            if parser is not None
            else CaptureHeaderParser()
        )



    def validate(
        self,
        data: bytes,
    ) -> CaptureHeaderValidationResult:
        """
        Validate Capture header from bytes.
        """

        issues: list[str] = []


        if not data:

            return CaptureHeaderValidationResult(
                valid=False,

                header_found=False,

                issues=(
                    "empty data",
                ),
            )


        try:

            header = self._parser.parse(
                data,
            )

        except Exception:

            return CaptureHeaderValidationResult(
                valid=False,

                header_found=False,

                issues=(
                    "unable to parse header",
                ),
            )


        if header is None:

            issues.append(
                "header not found"
            )


        return CaptureHeaderValidationResult(
            valid=(
                header is not None
            ),

            header_found=(
                header is not None
            ),

            issues=tuple(
                issues
            ),

            header=header,
        )



    def validate_file(
        self,
        path,
    ) -> CaptureHeaderValidationResult:
        """
        Validate a Capture file.
        """

        return self.validate(
            path.read_bytes()
        )