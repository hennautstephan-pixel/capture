from capture_recovery.reconstruction import (
    CorpusObjectIndexer,
    ParserObjectExtractor,
)


class FakeObject:

    def __init__(
        self,
        object_type,
        offset,
        size,
    ):
        self.object_type = object_type
        self.offset = offset
        self.size = size



class FakeParser:

    def parse(
        self,
        data,
    ):

        return [
            FakeObject(
                "fixture",
                4,
                7,
            )
        ]



def test_corpus_object_indexer(tmp_path):

    sample = tmp_path / "sample.c2p"

    sample.write_bytes(
        b"AAAAFIXTUREBBBB"
    )


    extractor = ParserObjectExtractor(
        FakeParser(),
    )


    indexer = CorpusObjectIndexer(
        extractor,
    )


    result = indexer.build(
        tmp_path,
    )


    assert (
        result.files_processed
        ==
        1
    )


    assert (
        result.objects_indexed
        ==
        1
    )


    assert (
        result.library.count()
        ==
        1
    )