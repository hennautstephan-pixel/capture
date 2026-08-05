from capture_recovery.research import (
    ReferenceCorpusBuilder,
    ReferenceCorpusBuildResult,
)



def test_reference_corpus_builder(tmp_path):

    project_a = tmp_path / "project_a.c2p"

    project_b = tmp_path / "project_b.c2p"


    project_a.write_bytes(
        b"CAPTURE_PROJECT_A"
    )

    project_b.write_bytes(
        b"CAPTURE_PROJECT_B"
    )


    result = (
        ReferenceCorpusBuilder(
            )
        .build(
            tmp_path
        )
    )


    assert isinstance(
        result,
        ReferenceCorpusBuildResult,
    )


    assert (
        result.projects_processed
        ==
        2
    )


    assert (
        result.objects_extracted
        >
        0
    )


    assert (
        len(result.corpus.projects)
        ==
        2
    )



def test_reference_corpus_builder_empty(tmp_path):

    result = (
        ReferenceCorpusBuilder()
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