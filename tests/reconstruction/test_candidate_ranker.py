from capture_recovery.reconstruction import (
    CandidateRanker,
    LibraryObject,
)



def test_candidate_ranker_prefers_type_and_size():

    candidates = (

        LibraryObject(
            object_type="camera",
            data=b"AAAA",
            source="camera.c2p",
        ),

        LibraryObject(
            object_type="fixture",
            data=b"BBBB",
            source="fixture.c2p",
        ),

    )


    ranker = CandidateRanker()


    result = ranker.best(
        candidates,
        object_type="fixture",
        size=4,
    )


    assert result is not None


    assert (
        result.object_type
        ==
        "fixture"
    )



def test_candidate_ranker_empty():

    ranker = CandidateRanker()


    result = ranker.best(
        (),
    )


    assert result is None