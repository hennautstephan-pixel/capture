from __future__ import annotations

from pathlib import Path

from capture_recovery.reconstruction.structured_object_extractor import (
    StructuredExtractedObject,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
    LibraryObject,
)


class ParserObjectExtractor:
    """
    Adapter between Capture ObjectParser output
    and reconstruction object structures.
    """

    def __init__(
        self,
        object_parser,
    ) -> None:

        self._parser = object_parser


    def extract_file(
        self,
        file_path: Path,
    ) -> tuple[StructuredExtractedObject, ...]:
        """
        Extract structured objects from parser output.
        """

        data = file_path.read_bytes()

        parsed_objects = self._parser.parse(
            data,
        )

        objects = []


        for item in parsed_objects:

            offset = getattr(
                item,
                "offset",
                0,
            )

            size = getattr(
                item,
                "size",
                0,
            )

            exact_size = getattr(
                item,
                "data_size",
                None,
            )


            if exact_size is not None:
                size = exact_size


            if size <= 0:
                continue


            block = data[
                offset:
                offset + size
            ]


            object_type = getattr(
                item,
                "object_type",
                "unknown",
            )


            objects.append(
                StructuredExtractedObject(
                    object_type=object_type,
                    offset=offset,
                    size=len(block),
                    data=block,
                    source=str(file_path),
                    signature=block[:16],
                )
            )


        return tuple(objects)



    def extract_to_library(
        self,
        file_path: Path,
        library: ObjectLibrary,
    ) -> int:
        """
        Extract objects and populate library.
        """

        objects = self.extract_file(
            file_path,
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


        return len(objects)