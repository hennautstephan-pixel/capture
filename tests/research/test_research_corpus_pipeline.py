from capture_recovery.research import (
    CorpusPipeline,
    CorpusPipelineResult,
)



def test_corpus_pipeline(tmp_path):

    project = tmp_path / "reference.c2p"


    project.write_bytes(
        b"CAPTURE_REFERENCE_PROJECT"
    )


    result = (
        CorpusPipeline()
        .build(
            tmp_path
        )
    )


    assert isinstance(
        result,
        CorpusPipelineResult,
    )


    assert (
        result.projects_processed
        ==
        1
    )


    assert (
        result.objects_extracted
        >
        0
    )


    assert (
        result.corpus.library
        is not None
    )



def test_corpus_pipeline_empty(tmp_path):

    result = (
        CorpusPipeline()
        .build(
            tmp_path
        )
    )


    assert (
        result.projects_processed
        ==
        0
    )


    assert (
        result.objects_extracted
        ==
        0
    )