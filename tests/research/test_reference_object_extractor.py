from capture_recovery.research import (
    ReferenceProjectAnalyzer,
    ReferenceObjectExtractor,
    ReferenceObject,
)



def test_reference_object_extractor(tmp_path):

    project = tmp_path / "reference.c2p"


    project.write_bytes(
        b"CAPTURE_REFERENCE_DATA"
    )


    model = (
        ReferenceProjectAnalyzer(
            block_size=8
        )
        .analyze(project)
    )


    extractor = ReferenceObjectExtractor()


    objects = extractor.extract(
        model
    )


    assert len(objects) == 3


    assert isinstance(
        objects[0],
        ReferenceObject,
    )


    assert (
        objects[0].offset
        ==
        0
    )


    assert (
        objects[0].size
        ==
        8
    )



def test_reference_object_has_signature(tmp_path):

    project = tmp_path / "reference.c2p"


    project.write_bytes(
        b"ABCDEFGH"
    )


    model = (
        ReferenceProjectAnalyzer(
            block_size=4
        )
        .analyze(project)
    )


    objects = (
        ReferenceObjectExtractor()
        .extract(model)
    )


    assert len(objects) == 2


    assert (
        objects[0].signature
        ==
        model.blocks[0].signature
    )