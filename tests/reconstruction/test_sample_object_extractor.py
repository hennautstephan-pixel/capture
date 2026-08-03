from capture_recovery.reconstruction import (
    SampleObjectExtractor,
    ObjectLibrary,
)


def test_extract_sample_file(tmp_path):

    sample = tmp_path / "sample.c2p"

    sample.write_bytes(
        b"CAPTURE_SAMPLE_OBJECT_DATA"
    )


    extractor = SampleObjectExtractor()


    objects = extractor.extract_file(
        sample,
    )


    assert len(objects) == 1

    assert (
        objects[0].source
        ==
        str(sample)
    )



def test_extract_directory_to_library(tmp_path):

    sample = tmp_path / "sample.c2p"

    sample.write_bytes(
        b"CAPTURE_SAMPLE_OBJECT_DATA"
    )


    library = ObjectLibrary()


    extractor = SampleObjectExtractor()


    count = extractor.extract_directory(
        tmp_path,
        library,
    )


    assert count == 1

    assert library.count() == 1