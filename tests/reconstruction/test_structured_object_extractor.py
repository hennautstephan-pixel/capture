from capture_recovery.reconstruction import (
    StructuredObjectExtractor,
    ObjectLibrary,
)


def test_structured_extractor_fallback(tmp_path):

    sample = tmp_path / "sample.c2p"

    sample.write_bytes(
        b"CAPTURE_STRUCTURED_SAMPLE"
    )


    extractor = StructuredObjectExtractor()


    objects = extractor.extract_file(
        sample,
    )


    assert len(objects) == 1

    assert (
        objects[0].object_type
        ==
        "unknown"
    )

    assert (
        objects[0].offset
        ==
        0
    )



def test_structured_extractor_populates_library(tmp_path):

    sample = tmp_path / "sample.c2p"

    sample.write_bytes(
        b"CAPTURE_STRUCTURED_SAMPLE"
    )


    extractor = StructuredObjectExtractor()

    library = ObjectLibrary()


    count = extractor.extract_directory(
        tmp_path,
        library,
    )


    assert count == 1

    assert library.count() == 1