"""
Tests detector protocol implementation.
"""

from capture_recovery.reverse.detector import (
    ReverseDetector,
)

from capture_recovery.reverse.numeric_detector import (
    NumericDetector,
)

from capture_recovery.reverse.string_detector import (
    StringDetector,
)

from capture_recovery.reverse.guid_detector import (
    GuidDetector,
)

from capture_recovery.reverse.alignment_detector import (
    AlignmentDetector,
)

from capture_recovery.reverse.entropy_detector import (
    EntropyDetector,
)



def test_numeric_detector():

    detector = NumericDetector()

    assert isinstance(
        detector,
        ReverseDetector,
    )

    assert detector.name == "numeric"



def test_string_detector():

    detector = StringDetector()

    assert isinstance(
        detector,
        ReverseDetector,
    )

    assert detector.name == "string"



def test_guid_detector():

    detector = GuidDetector()

    assert isinstance(
        detector,
        ReverseDetector,
    )

    assert detector.name == "guid"



def test_alignment_detector():

    detector = AlignmentDetector()

    assert isinstance(
        detector,
        ReverseDetector,
    )

    assert detector.name == "alignment"



def test_entropy_detector():

    detector = EntropyDetector()

    assert isinstance(
        detector,
        ReverseDetector,
    )

    assert detector.name == "entropy"