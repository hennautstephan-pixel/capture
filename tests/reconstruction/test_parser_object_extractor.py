from pathlib import Path

from capture_recovery.reconstruction import (
    ParserObjectExtractor,
    ObjectLibrary,
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



def test_parser_object_extractor():

    sample = Path(
        "sample.c2p"
    )

    sample.write_bytes(
        b"AAAAFIXTUREBBBB"
    )


    extractor = ParserObjectExtractor(
        FakeParser(),
    )


    objects = extractor.extract_file(
        sample,
    )


    assert len(objects) == 1

    assert (
        objects[0].object_type
        ==
        "fixture"
    )

    assert (
        objects[0].offset
        ==
        4
    )

    assert (
        objects[0].data
        ==
        b"FIXTURE"
    )