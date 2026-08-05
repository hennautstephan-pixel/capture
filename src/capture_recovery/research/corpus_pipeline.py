from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


from capture_recovery.research.reference_corpus_builder import (
    ReferenceCorpus,
    ReferenceCorpusBuilder,
)



@dataclass(frozen=True, slots=True)
class CorpusPipelineResult:
    """
    Result of corpus processing.
    """

    directory: Path

    projects_processed: int

    objects_extracted: int

    corpus: ReferenceCorpus



class CorpusPipeline:
    """
    High level corpus generation pipeline.

    Responsibilities:
    - validate corpus directory
    - build reference corpus
    - expose reconstruction library
    """



    def __init__(
        self,
        builder: ReferenceCorpusBuilder | None = None,
    ) -> None:

        self._builder = (
            builder
            if builder is not None
            else ReferenceCorpusBuilder()
        )



    def build(
        self,
        directory: Path,
    ) -> CorpusPipelineResult:
        """
        Build a complete corpus.
        """

        if not directory.exists():

            raise FileNotFoundError(
                directory
            )


        if not directory.is_dir():

            raise NotADirectoryError(
                directory
            )


        result = self._builder.build(
            directory,
        )


        return CorpusPipelineResult(
            directory=directory,
            projects_processed=(
                result.projects_processed
            ),
            objects_extracted=(
                result.objects_extracted
            ),
            corpus=result.corpus,
        )