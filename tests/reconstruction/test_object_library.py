from capture_recovery.reconstruction import (
    ObjectLibrary,
    LibraryObject,
)


def test_object_library_add_and_count():

    library = ObjectLibrary()

    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"ABC",
            source="sample.c2p",
        )
    )


    assert library.count() == 1



def test_object_library_find_by_type():

    library = ObjectLibrary()


    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"PROJECTOR",
            source="projecteur.c2p",
        )
    )


    result = library.find(
        object_type="fixture",
    )


    assert result is not None

    assert result.data == b"PROJECTOR"



def test_object_library_find_by_size():

    library = ObjectLibrary()


    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"1234",
            source="sample.c2p",
        )
    )


    result = library.find(
        object_type="fixture",
        size=4,
    )


    assert result is not None

    assert result.source == "sample.c2p"