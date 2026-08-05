from capture_recovery.cli import (
    CorpusLoader,
)



def test_corpus_loader_builds_cache(tmp_path):

    project = (
        tmp_path /
        "reference.c2p"
    )


    project.write_bytes(
        b"CAPTURE_REFERENCE_PROJECT"
    )


    loader = CorpusLoader()


    result = loader.load(
        tmp_path,
    )


    cache = (
        tmp_path /
        "corpus.json"
    )


    assert cache.exists()


    assert (
        result.files_processed
        ==
        1
    )


    assert (
        result.objects_loaded
        >
        0
    )



def test_corpus_loader_loads_existing_cache(tmp_path):

    project = (
        tmp_path /
        "reference.c2p"
    )


    project.write_bytes(
        b"CAPTURE_REFERENCE_PROJECT"
    )


    loader = CorpusLoader()


    first = loader.load(
        tmp_path,
    )


    second = loader.load(
        tmp_path,
    )


    assert (
        second.objects_loaded
        ==
        first.objects_loaded
    )



def test_corpus_loader_missing_directory(tmp_path):

    missing = (
        tmp_path /
        "missing"
    )


    try:

        CorpusLoader().load(
            missing
        )

    except FileNotFoundError:

        assert True

    else:

        assert False