from capture_recovery.reconstruction import (
    ObjectLibrary,
    LibraryObject,
    ReconstructionPlanner,
    ReconstructionPlan,
)

from capture_recovery.recovery import (
    IntelligentRestoreAction,
)



def test_reconstruction_planner_finds_object():

    library = ObjectLibrary()


    library.add(
        LibraryObject(
            object_type="fixture",
            data=b"FIXTURE_DATA",
            source="sample.c2p",
        )
    )


    planner = ReconstructionPlanner(
        library,
    )


    action = IntelligentRestoreAction(
        offset=100,
        size=12,
        object_type="fixture",
        confidence=0.95,
    )


    plan = planner.plan(
        action,
    )


    assert isinstance(
        plan,
        ReconstructionPlan,
    )


    assert (
        plan.object_type
        ==
        "fixture"
    )


    assert (
        plan.replacement
        ==
        b"FIXTURE_DATA"
    )


    assert (
        plan.source
        ==
        "sample.c2p"
    )



def test_reconstruction_planner_returns_none():

    library = ObjectLibrary()


    planner = ReconstructionPlanner(
        library,
    )


    action = IntelligentRestoreAction(
        offset=0,
        size=10,
        object_type="unknown",
        confidence=0.9,
    )


    assert (
        planner.plan(action)
        is None
    )