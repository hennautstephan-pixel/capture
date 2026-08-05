from __future__ import annotations

from dataclasses import dataclass


from capture_recovery.formats.capture.stream_parser import (
    CaptureStreamParser,
)



@dataclass(frozen=True, slots=True)
class CaptureStreamValidationResult:
    """
    Result of Capture stream validation.
    """

    valid: bool

    streams_found: int

    issues: tuple[str, ...]

    streams: tuple = ()



class CaptureStreamValidator:
    """
    Validate Capture binary streams.
    """



    def __init__(
        self,
        parser: CaptureStreamParser | None = None,
    ) -> None:

        self._parser = (
            parser
            if parser is not None
            else CaptureStreamParser()
        )



    def validate(
        self,
        data: bytes,
    ) -> CaptureStreamValidationResult:
        """
        Validate streams contained
        in Capture binary data.
        """

        if not data:

            return CaptureStreamValidationResult(
                valid=False,

                streams_found=0,

                issues=(
                    "empty data",
                ),
            )


        try:

            streams = self._parser.parse(
                data,
            )


        except Exception:

            return CaptureStreamValidationResult(
                valid=False,

                streams_found=0,

                issues=(
                    "unable to parse streams",
                ),
            )


        if streams is None:

            streams = []


        streams = tuple(
            streams
        )


        issues: list[str] = []


        if len(streams) == 0:

            issues.append(
                "no streams found"
            )


        return CaptureStreamValidationResult(
            valid=(
                len(streams) > 0
            ),

            streams_found=len(
                streams
            ),

            issues=tuple(
                issues
            ),

            streams=streams,
        )



    def validate_file(
        self,
        path,
    ) -> CaptureStreamValidationResult:
        """
        Validate streams from a Capture file.
        """

        return self.validate(
            path.read_bytes()
        )