from capture_recovery.reconstruction import (
    ObjectLibrary,
    LibraryObject,
    ReconstructionStrategy,
    CorruptionRegion,
)



def test_strategy_selects_candidate():

    library = ObjectLibrary()


    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"FIXTURE_DATA",
            source="reference.c2p",
        )
    )


    strategy = ReconstructionStrategy(
        library,
    )


    decision = strategy.build(
        CorruptionRegion(
            offset=10,
            size=12,
        ),

        object_type="fixture",
    )


    assert decision is not None

    assert decision.object_type == "fixture"

    assert decision.replacement == b"FIXTURE_DATA"



def test_strategy_without_candidate():

    library = ObjectLibrary()


    strategy = ReconstructionStrategy(
        library,
    )


    decision = strategy.build(
        CorruptionRegion(
            offset=0,
            size=10,
        ),

        object_type="unknown",
    )


    assert decision is None