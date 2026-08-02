from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class CaptureHeader:
    """
    Raw Capture (.c2p) file header.

    Only fields that are observable on every analysed sample
    are represented here.
    """

    file_size: int

    project_tag: str

    format_version: int

    software_tag: str

    software_tag_version: int

    first_stream_offset: int

    reserved: bytes = field(default_factory=bytes)

    raw: bytes = field(default_factory=bytes)

    @property
    def header_size(self) -> int:
        return len(self.raw)

    @property
    def has_reserved_bytes(self) -> bool:
        return bool(self.reserved)

    def validate_size(
        self,
        actual_size: int,
    ) -> bool:
        return self.file_size == actual_size

    def validate(self, actual_size: int) -> tuple[str, ...]:
        """
        Validate the header against the current file.
        """

        errors: list[str] = []

        if self.file_size != actual_size:
            errors.append("Invalid file size.")

        if self.project_tag != "Project":
            errors.append("Invalid Project tag.")

        if self.software_tag != "SoftwareVersion":
            errors.append("Invalid SoftwareVersion tag.")

        if self.first_stream_offset <= 0:
            errors.append("Invalid first stream offset.")

        return tuple(errors)

    @property
    def is_valid(self) -> bool:
        return (
            self.project_tag == "Project"
            and self.software_tag == "SoftwareVersion"
            and self.first_stream_offset > 0
        )