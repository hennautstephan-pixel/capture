from capture_recovery.research import (
    CorpusPipeline,
    CorpusStore,
)



def test_corpus_store_save_load(tmp_path):

    project = (
        tmp_path /
        "reference.c2p"
    )

    project.write_bytes(
        b"CAPTURE_REFERENCE_PROJECT"
    )


    corpus = (
        CorpusPipeline()
        .build(
            tmp_path
        )
        .corpus
    )


    store_file = (
        tmp_path /
        "corpus.json"
    )


    store = CorpusStore()


    store.save(
        corpus,
        store_file,
    )


    assert store_file.exists()


    loaded = store.load(
        store_file,
    )


    assert (
        len(
            loaded.objects
        )
        ==
        len(
            corpus.objects
        )
    )



def test_corpus_store_empty(tmp_path):

    corpus_file = (
        tmp_path /
        "empty.json"
    )


    corpus_file.write_text(
        """
        {
            "version": 1,
            "projects": [],
            "objects": []
        }
        """,
        encoding="utf-8",
    )


    corpus = (
        CorpusStore()
        .load(
            corpus_file
        )
    )


    assert (
        len(corpus.objects)
        ==
        0
    )