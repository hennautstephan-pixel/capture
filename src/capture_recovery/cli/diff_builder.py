from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ByteDifference:
    """
    One byte difference between two files.
    """

    offset: int

    original: int

    current: int



@dataclass(slots=True, frozen=True)
class StreamDiff:
    """
    Binary comparison result.

    Compatible with DiffAnalyzer.
    """

    differences: tuple[ByteDifference, ...]

    @property
    def identical(self) -> bool:
        """
        Return True when files are identical.
        """

        return not bool(
            self.differences
        )



class DiffBuilder:
    """
    Build binary differences between
    Capture files.
    """


    def compare(
        self,
        source: Path,
        reference: Path,
    ) -> StreamDiff:
        """
        Compare two binary files.
        """

        source_data = source.read_bytes()

        reference_data = reference.read_bytes()


        differences = []


        max_size = max(
            len(source_data),
            len(reference_data),
        )


        for offset in range(max_size):

            source_byte = (
                source_data[offset]
                if offset < len(source_data)
                else -1
            )


            reference_byte = (
                reference_data[offset]
                if offset < len(reference_data)
                else -1
            )


            if source_byte != reference_byte:

                differences.append(
                    ByteDifference(
                        offset=offset,
                        original=reference_byte,
                        current=source_byte,
                    )
                )


        return StreamDiff(
            differences=tuple(
                differences
            )
        )