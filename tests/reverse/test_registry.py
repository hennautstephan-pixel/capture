"""
Tests for ReverseRegistry.
"""

from __future__ import annotations


from capture_recovery.reverse.registry import (
    ReverseRegistry,
)



class FakeDetector:
    pass



class OtherDetector:
    pass



def test_empty_registry():

    registry = ReverseRegistry()

    assert len(registry) == 0



def test_register_detector():

    registry = ReverseRegistry()

    detector = FakeDetector()

    registry.register(
        detector
    )


    assert len(registry) == 1



def test_duplicate_register():

    registry = ReverseRegistry()

    detector = FakeDetector()

    registry.register(
        detector
    )

    registry.register(
        detector
    )


    assert len(registry) == 1



def test_unregister():

    registry = ReverseRegistry()

    detector = FakeDetector()

    registry.register(
        detector
    )

    registry.unregister(
        detector
    )


    assert len(registry) == 0



def test_get_detector():

    registry = ReverseRegistry()

    detector = FakeDetector()

    registry.register(
        detector
    )


    result = registry.get(
        FakeDetector
    )


    assert result is detector



def test_get_unknown_detector():

    registry = ReverseRegistry()


    assert (
        registry.get(
            FakeDetector
        )
        is None
    )



def test_all_detectors():

    first = FakeDetector()
    second = OtherDetector()


    registry = ReverseRegistry(
        (
            first,
            second,
        )
    )


    assert registry.all() == (
        first,
        second,
    )



def test_clear():

    registry = ReverseRegistry(
        (
            FakeDetector(),
        )
    )


    registry.clear()


    assert len(registry) == 0