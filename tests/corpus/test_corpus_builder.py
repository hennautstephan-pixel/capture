from capture_recovery.corpus import (
    Corpus,
    CorpusBuilder,
)


def test_empty(tmp_path):

    corpus = CorpusBuilder().build(tmp_path)

    assert isinstance(
        corpus,
        Corpus,
    )

    assert corpus.count == 0


def test_directory(tmp_path):

    path = tmp_path / "sample.bin"

    path.write_bytes(
        b"1234"
    )

    corpus = CorpusBuilder().build(tmp_path)

    assert corpus.count == 1