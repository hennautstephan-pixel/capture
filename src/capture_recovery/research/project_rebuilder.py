from __future__ import annotations

from dataclasses import dataclass

from .repair_plan import ExecutionPlan
from .stream_rebuilder import StreamRebuildResult


@dataclass(slots=True, frozen=True)
class ProjectImage:
    """
    Complete rebuilt project image.
    """

    header: bytes

    stream: bytes

    footer: bytes

    @property
    def data(self) -> bytes:
        return (
            self.header
            + self.stream
            + self.footer
        )

    @property
    def size(self) -> int:
        return len(self.data)

    @property
    def is_empty(self) -> bool:
        """
        Return True if the rebuilt image contains no data.
        """
        return self.size == 0

    def sections(self) -> tuple[bytes, bytes, bytes]:
        """
        Return the project sections.

        Future rebuilders can manipulate the sections
        independently without accessing the attributes
        directly.
        """
        return (
            self.header,
            self.stream,
            self.footer,
        )


@dataclass(slots=True, frozen=True)
class ProjectRebuildResult:
    """
    Result of a project reconstruction.
    """

    image: ProjectImage

    repaired: bool

    warnings: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """
        Return True if the rebuilt project contains the
        minimum required components.
        """
        return (
            len(self.image.header) > 0
            and len(self.image.stream) > 0
        )

    @property
    def warning_count(self) -> int:
        """
        Number of warnings generated during rebuilding.
        """
        return len(self.warnings)


class ProjectRebuilder:
    """
    Assemble a repaired Capture project.
    """

    def rebuild(
        self,
        plan: ExecutionPlan,
        header: bytes,
        stream: StreamRebuildResult,
        footer: bytes,
    ) -> ProjectRebuildResult:

        warnings: list[str] = []

        image = ProjectImage(
            header=header,
            stream=stream.stream,
            footer=footer,
        )

        repaired = stream.repaired_objects > 0

        warnings.extend(stream.warnings)

        if not header:
            warnings.append("Missing header.")

        if not stream.stream:
            warnings.append("Missing stream.")

        if not footer:
            warnings.append("Missing footer.")

        return ProjectRebuildResult(
            image=image,
            repaired=repaired,
            warnings=tuple(warnings),
        )