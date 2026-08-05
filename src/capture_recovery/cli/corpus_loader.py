from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.research import (
    CorpusPipeline,
    CorpusStore,
    ReferenceCorpus,
)



@dataclass(frozen=True, slots=True)
class CorpusLoadResult:
    """
    Result returned by CLI corpus loading.
    """

    directory: Path

    files_processed: int

    objects_loaded: int

    corpus: ReferenceCorpus


    @property
    def library(self):
        """
        Access reconstruction library.
        """

        return self.corpus.library



class CorpusLoader:
    """
    CLI adapter for persistent corpus loading.

    Workflow:

    1. Load existing corpus cache.
    2. Otherwise build corpus.
    3. Save generated corpus.
    """



    DEFAULT_CACHE_NAME = "corpus.json"



    def __init__(
        self,
        pipeline: CorpusPipeline | None = None,
        store: CorpusStore | None = None,
    ) -> None:

        self._pipeline = (
            pipeline
            if pipeline is not None
            else CorpusPipeline()
        )

        self._store = (
            store
            if store is not None
            else CorpusStore()
        )



    def load(
        self,
        directory: Path,
        *,
        cache_path: Path | None = None,
    ) -> CorpusLoadResult:
        """
        Load or build corpus.
        """

        if not directory.exists():

            raise FileNotFoundError(
                directory
            )


        if not directory.is_dir():

            raise NotADirectoryError(
                directory
            )


        if cache_path is None:

            cache_path = (
                directory /
                self.DEFAULT_CACHE_NAME
            )



        if cache_path.exists():

            corpus = self._store.load(
                cache_path
            )

            return CorpusLoadResult(
                directory=directory,
                files_processed=len(
                    corpus.projects
                ),
                objects_loaded=len(
                    corpus.objects
                ),
                corpus=corpus,
            )



        result = self._pipeline.build(
            directory
        )


        self._store.save(
            result.corpus,
            cache_path,
        )


        return CorpusLoadResult(
            directory=directory,
            files_processed=(
                result.projects_processed
            ),
            objects_loaded=(
                result.objects_extracted
            ),
            corpus=result.corpus,
        )