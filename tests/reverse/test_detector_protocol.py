"""
Tests for ReverseDetector protocol.
"""

from __future__ import annotations


from capture_recovery.reverse.detector import (
    ReverseDetector,
)



class ValidDetector:
    """
    Detector implementing protocol.
    """


    @property
    def name(self) -> str:

        return "valid"



    def detect(
        self,
        data,
        options=None,
    ):

        return []



class InvalidDetector:
    pass



def test_valid_detector_matches_protocol():

    detector = ValidDetector()


    assert isinstance(
        detector,
        ReverseDetector,
    )



def test_invalid_detector_does_not_match():

    detector = InvalidDetector()


    assert not isinstance(
        detector,
        ReverseDetector,
    )



def test_detector_name():

    detector = ValidDetector()


    assert detector.name == "valid"



def test_detector_returns_list():

    detector = ValidDetector()


    result = detector.detect(
        b"test"
    )


    assert result == []