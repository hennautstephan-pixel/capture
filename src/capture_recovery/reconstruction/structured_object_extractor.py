from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)


@dataclass(slots=True, frozen=True)
class StructuredExtractedObject:
    """
    Structured object extracted from a Capture file.
    """

    object_type: str

    offset: int

    size: int

    data: bytes

    source: str

    signature: bytes



class StructuredObjectExtractor:
    """
    Extract structured objects from Capture files.

    This extractor works with parser output when
    available and stores reusable objects in an
    ObjectLibrary.

    No repair is performed here.
    """

    def __init__(
        self,
        object_parser=None,
        *,
        minimum_size: int = 8,
    ) -> None:

        self._parser = object_parser

        self._minimum_size = minimum_size



    def extract_file(
        self,
        file_path: Path,
    ) -> tuple[StructuredExtractedObject, ...]:
        """
        Extract objects from one Capture file.
        """

        data = file_path.read_bytes()


        if self._parser is None:

            return self._fallback_extract(
                data,
                file_path,
            )


        parsed_objects = self._parser.parse(
            data,
        )


        objects = []


        for item in parsed_objects:

            offset = item.offset

            size = item.size


            block = data[
                offset:
                offset + size
            ]


            if len(block) < self._minimum_size:

                continue


            objects.append(
                StructuredExtractedObject(
                    object_type=item.object_type,
                    offset=offset,
                    size=size,
                    data=block,
                    source=str(file_path),
                    signature=block[:16],
                )
            )


        return tuple(objects)



    def add_to_library(
        self,
        objects: tuple[
            StructuredExtractedObject,
            ...,
        ],
        library: ObjectLibrary,
    ) -> int:
        """
        Add extracted objects to a library.
        """

        count = 0


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



    def extract_directory(
        self,
        directory: Path,
        library: ObjectLibrary,
    ) -> int:
        """
        Extract all Capture samples.
        """

        total = 0


        for file_path in sorted(
            directory.glob("*.c2p")
        ):

            objects = self.extract_file(
                file_path,
            )


            total += self.add_to_library(
                objects,
                library,
            )


        return total



    def _fallback_extract(
        self,
        data: bytes,
        source: Path,
    ) -> tuple[StructuredExtractedObject, ...]:
        """
        Temporary fallback until the parser
        exposes structured object regions.
        """

        if len(data) < self._minimum_size:

            return ()


        return (
            StructuredExtractedObject(
                object_type="unknown",
                offset=0,
                size=len(data),
                data=data,
                source=str(source),
                signature=data[:16],
            ),
        )