from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.io import CaptureBinaryReader


@dataclass(slots=True, frozen=True)
class StreamDifference:
    """
    Single byte difference.
    """

    offset: int

    left: int

    right: int


@dataclass(slots=True, frozen=True)
class StreamDiff:
    """
    Result of a binary stream comparison.
    """

    left_size: int

    right_size: int

    differences: tuple[StreamDifference, ...]

    @property
    def identical(self) -> bool:
        return not self.differences

    @property
    def difference_count(self) -> int:
        return len(self.differences)


class StreamDiffer:
    """
    Compare binary streams.

    Accepts:
    - bytes
    - pathlib.Path
    - string paths
    """

    def __init__(self) -> None:

        self._reader = CaptureBinaryReader()


    def compare(
        self,
        left: bytes | str | Path,
        right: bytes | str | Path,
    ) -> StreamDiff:

        left_data = self._load(left)

        right_data = self._load(right)

        differences = []

        size = max(
            len(left_data),
            len(right_data),
        )

        for offset in range(size):

            left_byte = (
                left_data[offset]
                if offset < len(left_data)
                else -1
            )

            right_byte = (
                right_data[offset]
                if offset < len(right_data)
                else -1
            )

            if left_byte != right_byte:

                differences.append(
                    StreamDifference(
                        offset=offset,
                        left=left_byte,
                        right=right_byte,
                    )
                )

        return StreamDiff(
            left_size=len(left_data),
            right_size=len(right_data),
            differences=tuple(differences),
        )


    def _load(
        self,
        value: bytes | str | Path,
    ) -> bytes:

        if isinstance(value, bytes):

            return value

        return self._reader.read(
            value,
        )