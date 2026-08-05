from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.formats.capture.section import (
    CaptureSection,
)


@dataclass(frozen=True, slots=True)
class CaptureSectionValidationResult:
    """
    Result of a Capture section validation.
    """

    valid: bool

    offset_valid: bool

    size_valid: bool

    content_valid: bool

    issues: tuple[str, ...] = ()


class CaptureSectionValidator:
    """
    Validate raw Capture sections.

    A section is considered valid when:
    - its offset is not negative
    - its declared size matches its payload
    - it contains coherent data
    """

    def validate(
        self,
        section: CaptureSection,
    ) -> CaptureSectionValidationResult:
        """
        Validate one Capture section.
        """

        issues: list[str] = []

        offset_valid = (
            section.offset >= 0
        )

        if not offset_valid:
            issues.append(
                "invalid section offset"
            )


        size_valid = (
            section.size >= 0
            and section.size == len(section.raw)
        )

        if not size_valid:
            issues.append(
                "section size mismatch"
            )


        content_valid = (
            section.raw is not None
            and len(section.raw) == section.size
        )

        if not content_valid:
            issues.append(
                "invalid section content"
            )


        return CaptureSectionValidationResult(
            valid=(
                offset_valid
                and size_valid
                and content_valid
            ),
            offset_valid=offset_valid,
            size_valid=size_valid,
            content_valid=content_valid,
            issues=tuple(issues),
        )