from capture_recovery.research import (
    ReferenceProjectAnalyzer,
    ReferenceObjectExtractor,
    ObjectSignatureIndex,
    SignatureLookupResult,
)



def test_object_signature_index(tmp_path):

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


    index = ObjectSignatureIndex()


    index.add_many(
        objects
    )


    assert (
        index.size
        ==
        len(objects)
    )


    result = index.find(
        objects[0].signature
    )


    assert isinstance(
        result,
        SignatureLookupResult,
    )


    assert result.found


    assert (
        result.object
        ==
        objects[0]
    )



def test_object_signature_index_missing():

    index = ObjectSignatureIndex()


    result = index.find(
        "unknown"
    )


    assert not result.found

    assert (
        result.object
        is None
    )