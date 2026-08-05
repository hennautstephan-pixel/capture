from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.research.reference_project_analyzer import (
    ReferenceProjectAnalyzer,
)

from capture_recovery.research.reference_object_extractor import (
    ReferenceObjectExtractor,
    ReferenceObject,
)

from capture_recovery.research.reference_library_builder import (
    ReferenceLibraryBuilder,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)



@dataclass(frozen=True, slots=True)
class ReferenceCorpus:
    """
    Complete reference corpus.

    Contains:
    - analysed projects
    - extracted objects
    - searchable library
    """

    projects: tuple[Path, ...]

    objects: tuple[ReferenceObject, ...]

    library: ObjectLibrary



@dataclass(frozen=True, slots=True)
class ReferenceCorpusBuildResult:
    """
    Result of corpus generation.
    """

    projects_processed: int

    objects_extracted: int

    corpus: ReferenceCorpus



class ReferenceCorpusBuilder:
    """
    Build a reconstruction corpus from
    valid Capture projects.
    """



    def __init__(
        self,
        analyzer: ReferenceProjectAnalyzer | None = None,
        extractor: ReferenceObjectExtractor | None = None,
        library_builder: ReferenceLibraryBuilder | None = None,
    ) -> None:

        self._analyzer = (
            analyzer
            if analyzer is not None
            else ReferenceProjectAnalyzer()
        )

        self._extractor = (
            extractor
            if extractor is not None
            else ReferenceObjectExtractor()
        )

        self._library_builder = (
            library_builder
            if library_builder is not None
            else ReferenceLibraryBuilder()
        )



    def build(
        self,
        directory: Path,
    ) -> ReferenceCorpusBuildResult:
        """
        Build corpus from a directory.
        """

        if not directory.exists():

            raise FileNotFoundError(
                directory
            )


        if not directory.is_dir():

            raise NotADirectoryError(
                directory
            )


        projects = tuple(
            sorted(
                directory.glob(
                    "*.c2p"
                )
            )
        )


        objects: list[ReferenceObject] = []


        for project in projects:

            model = self._analyzer.analyze(
                project
            )


            extracted = self._extractor.extract(
                model
            )


            objects.extend(
                extracted
            )


        library_result = (
            self._library_builder.build(
                tuple(objects)
            )
        )


        corpus = ReferenceCorpus(
            projects=projects,
            objects=tuple(objects),
            library=library_result.library,
        )


        return ReferenceCorpusBuildResult(
            projects_processed=len(projects),
            objects_extracted=len(objects),
            corpus=corpus,
        )