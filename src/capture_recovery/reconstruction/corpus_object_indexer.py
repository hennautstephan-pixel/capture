from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)

from capture_recovery.reconstruction.parser_object_extractor import (
    ParserObjectExtractor,
)


@dataclass(slots=True, frozen=True)
class CorpusIndexResult:
    """
    Result of corpus indexing.
    """

    directory: Path

    files_processed: int

    objects_indexed: int

    library: ObjectLibrary



class CorpusObjectIndexer:
    """
    Build an ObjectLibrary from a Capture corpus.

    This class is responsible for corpus traversal.
    Object extraction is delegated to
    ParserObjectExtractor.
    """

    def __init__(
        self,
        object_extractor: ParserObjectExtractor,
    ) -> None:

        self._extractor = object_extractor



    def build(
        self,
        directory: Path,
    ) -> CorpusIndexResult:
        """
        Index every Capture file in a directory.
        """

        library = ObjectLibrary()

        files_processed = 0

        objects_indexed = 0


        for file_path in sorted(
            directory.glob("*.c2p")
        ):

            files_processed += 1


            objects_indexed += (
                self._extractor.extract_to_library(
                    file_path,
                    library,
                )
            )


        return CorpusIndexResult(
            directory=directory,
            files_processed=files_processed,
            objects_indexed=objects_indexed,
            library=library,
        )