from capture_recovery.research import (
    ReferenceProjectAnalyzer,
    ReferenceObjectExtractor,
    ReferenceLibraryBuilder,
    ReferenceLibraryResult,
)



def test_reference_library_builder(tmp_path):

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


    objects = (
        ReferenceObjectExtractor()
        .extract(model)
    )


    result = (
        ReferenceLibraryBuilder()
        .build(objects)
    )


    assert isinstance(
        result,
        ReferenceLibraryResult,
    )


    assert (
        result.objects_added
        ==
        len(objects)
    )


    assert result.library is not None



def test_reference_library_builder_empty():

    result = (
        ReferenceLibraryBuilder()
        .build(())
    )


    assert (
        result.objects_added
        ==
        0
    )

    assert result.library is not None