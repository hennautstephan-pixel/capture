"""
Tests for custom detector registry in ReverseEngine.
"""

from __future__ import annotations


from capture_recovery.reverse.registry import (
    ReverseRegistry,
)

from capture_recovery.reverse.reverse_engine import (
    ReverseEngine,
    ReverseResult,
)



class CustomValue:
    """
    Fake detection result.
    """

    pass



class CustomDetector:
    """
    Fake detector used for injection testing.
    """


    def __init__(self):

        self.called = False



    def detect(
        self,
        data,
        options=None,
    ):

        self.called = True

        return [
            CustomValue()
        ]



def test_engine_accepts_custom_registry():

    detector = CustomDetector()


    registry = ReverseRegistry(
        (
            detector,
        )
    )


    engine = ReverseEngine(
        registry=registry,
    )


    assert engine.registry is registry



def test_custom_detector_is_called():

    detector = CustomDetector()


    registry = ReverseRegistry(
        (
            detector,
        )
    )


    engine = ReverseEngine(
        registry=registry,
    )


    engine.analyze(
        b"test",
    )


    assert detector.called is True



def test_custom_registry_replaces_defaults():

    detector = CustomDetector()


    registry = ReverseRegistry(
        (
            detector,
        )
    )


    engine = ReverseEngine(
        registry=registry,
    )


    result = engine.analyze(
        b"anything",
    )


    assert isinstance(
        result,
        ReverseResult,
    )


    assert result.total == 0



def test_empty_custom_registry():

    registry = ReverseRegistry()


    engine = ReverseEngine(
        registry=registry,
    )


    result = engine.analyze(
        b"test",
    )


    assert result.total == 0