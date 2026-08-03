from capture_recovery.reconstruction import (
    ObjectReconstructor,
    ReconstructedObject,
)

from capture_recovery.recovery import (
    IntelligentRestoreAction,
)



class FakeObject:

    def __init__(
        self,
        data,
        source,
    ):

        self.data = data

        self.source = source



class FakeLibrary:

    def find(
        self,
        object_type,
        size,
    ):

        return FakeObject(
            data=b"OBJECT_DATA",
            source="sample.c2p",
        )



def test_object_reconstructor_finds_object():

    library = FakeLibrary()


    reconstructor = ObjectReconstructor(
        library,
    )


    action = IntelligentRestoreAction(
        offset=100,
        size=10,
        object_type="fixture",
        confidence=0.95,
    )


    result = reconstructor.reconstruct(
        action,
    )


    assert isinstance(
        result,
        ReconstructedObject,
    )


    assert (
        result.object_type
        ==
        "fixture"
    )


    assert (
        result.data
        ==
        b"OBJECT_DATA"
    )


    assert (
        result.source
        ==
        "sample.c2p"
    )