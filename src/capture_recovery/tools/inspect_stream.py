from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.io import CaptureBinaryReader
from capture_recovery.parser import (
    BinaryCursor,
    StreamDecompressor,
)


@dataclass(slots=True, frozen=True)
class StreamInspection:
    """
    Result of a stream inspection.
    """

    file: Path

    compressed_size: int

    decompressed_size: int

    printable_bytes: int

    zero_bytes: int

    printable_ratio: float

    zero_ratio: float

    first_bytes: bytes

    @property
    def is_empty(self) -> bool:
        return self.decompressed_size == 0


class StreamInspector:
    """
    Inspect a decompressed Capture stream.
    """

    PREVIEW_SIZE = 64

    def __init__(self) -> None:

        self._reader = CaptureBinaryReader()

        self._decompressor = StreamDecompressor()

    def inspect(
        self,
        path: str | Path,
    ) -> StreamInspection:

        path = Path(path)

        compressed = self._reader.read(path)

        stream = self._decompressor.decompress(
            compressed,
        )

        data = stream.decompressed

        cursor = BinaryCursor(data)

        preview = cursor.read_bytes(
            min(
                self.PREVIEW_SIZE,
                cursor.remaining,
            )
        )

        printable = sum(
            32 <= value <= 126
            for value in data
        )

        zeros = data.count(0)

        size = len(data)

        printable_ratio = (
            printable / size
            if size
            else 0.0
        )

        zero_ratio = (
            zeros / size
            if size
            else 0.0
        )

        return StreamInspection(
            file=path,
            compressed_size=stream.compressed_size,
            decompressed_size=size,
            printable_bytes=printable,
            zero_bytes=zeros,
            printable_ratio=printable_ratio,
            zero_ratio=zero_ratio,
            first_bytes=preview,
        )

    @staticmethod
    def print(
        inspection: StreamInspection,
    ) -> None:

        print(f"File               : {inspection.file}")
        print(f"Compressed size    : {inspection.compressed_size}")
        print(f"Decompressed size  : {inspection.decompressed_size}")
        print(f"Printable bytes    : {inspection.printable_bytes}")
        print(f"Zero bytes         : {inspection.zero_bytes}")
        print(f"Printable ratio    : {inspection.printable_ratio:.2%}")
        print(f"Zero ratio         : {inspection.zero_ratio:.2%}")
        print()
        print("First bytes")
        print("-----------")
        print(inspection.first_bytes.hex(" "))


def main() -> None:

    import argparse

    parser = argparse.ArgumentParser(
        description="Inspect a Capture stream.",
    )

    parser.add_argument(
        "file",
        type=Path,
    )

    args = parser.parse_args()

    inspector = StreamInspector()

    result = inspector.inspect(
        args.file,
    )

    inspector.print(
        result,
    )


if __name__ == "__main__":

    main()