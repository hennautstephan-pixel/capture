from capture_recovery.reconstruction import (
    ObjectLibrary,
)

from capture_recovery.research import (
    ReferenceProjectAnalyzer,
    ReferenceObjectExtractor,
)



def test_object_library_signature_lookup(tmp_path):

    project = (
        tmp_path /
        "reference.c2p"
    )


    project.write_bytes(
        b"CAPTURE_REFERENCE_DATA"
    )


    model = (
        ReferenceProjectAnalyzer(
            block_size=8
        )
        .analyze(project)
    )


    objects = (
        ReferenceObjectExtractor()
        .extract(model)
    )


    library = ObjectLibrary()


    library.add_many(
        objects
    )


    assert (
        library.size
        ==
        len(objects)
    )


    result = (
        library.find_by_signature(
            objects[0].signature
        )
    )


    assert result.found


    assert (
        result.object
        ==
        objects[0]
    )



def test_object_library_empty():

    library = ObjectLibrary()


    assert (
        library.size
        ==
        0
    )


    assert not (
        library.contains_signature(
            "unknown"
        )
    )