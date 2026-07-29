from __future__ import annotations

from .segment import Segment


class BinaryReport:

    @staticmethod
    def generate(segments: list[Segment]) -> str:

        if not segments:
            return "No segments detected."

        lines = [
            "Offset      Length    Type        Details",
            "-" * 45,
        ]

        for segment in sorted(segments, key=lambda s: s.offset):

            value = segment.metadata.get("value", "")

            details = repr(value) if value != "" else ""

            lines.append(
                f"{segment.offset:08X}  "
                f"{segment.length:6d}    "
                f"{segment.kind:<10}  "
                f"{details}"
            )

        return "\n".join(lines)