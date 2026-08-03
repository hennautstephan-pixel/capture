from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)


@dataclass(slots=True, frozen=True)
class ExtractedObject:
    """
    Object extracted from a sample file.
    """

    object_type: str

    data: bytes

    source: str

    signature: bytes



class SampleObjectExtractor:
    """
    Extract reusable objects from Capture samples.

    This first implementation extracts
    binary regions as candidate objects.

    Object semantic identification will be
    improved later using the Capture parser.
    """


    def __init__(
        self,
        *,
        minimum_size: int = 16,
    ) -> None:

        self._minimum_size = minimum_size



    def extract_file(
        self,
        sample: Path,
    ) -> tuple[ExtractedObject, ...]:
        """
        Extract objects from one sample file.
        """

        data = sample.read_bytes()


        if len(data) < self._minimum_size:

            return ()


        signature = (
            data[:16]
            if len(data) >= 16
            else data
        )


        return (
            ExtractedObject(
                object_type="unknown",
                data=data,
                source=str(sample),
                signature=signature,
            ),
        )



    def extract_directory(
        self,
        directory: Path,
        library: ObjectLibrary,
    ) -> int:
        """
        Extract all samples from a directory
        and populate an ObjectLibrary.
        """

        count = 0


        for sample in sorted(
            directory.glob("*.c2p")
        ):

            objects = self.extract_file(
                sample,
            )


            for obj in objects:

                library.add(
                    LibraryObject(
                        object_type=obj.object_type,
                        data=obj.data,
                        source=obj.source,
                        signature=obj.signature,
                    )
                )

                count += 1


        return count