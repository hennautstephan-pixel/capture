from capture_recovery.reconstruction import (
    ObjectLibrary,
    LibraryObject,
    ReconstructionStrategy,
    RecoveryOrchestrator,
)



def test_recovery_orchestrator_repairs_region():

    library = ObjectLibrary()


    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"XX",
            source="reference.c2p",
        )
    )


    strategy = ReconstructionStrategy(
        library,
    )


    orchestrator = RecoveryOrchestrator(
        strategy=strategy,
    )


    result = orchestrator.recover(
        b"AABBCC",

        b"AAXXCC",

        object_type="fixture",
    )


    assert result.data == b"AAXXCC"

    assert len(result.decisions) == 1

    assert result.success is True