"""
Tests for alignment_detector.
"""

from __future__ import annotations


from capture_recovery.reverse.alignment_detector import (
    AlignmentDetector,
)



# ----------------------------------------------------------------------
# Basic detection
# ----------------------------------------------------------------------


def test_detect_alignments() -> None:

    detector = AlignmentDetector(
        alignments=(
            2,
            4,
        )
    )


    result = detector.detect(
        bytes(64),
    )


    assert len(result) > 0



def test_detect_alignment_value() -> None:

    detector = AlignmentDetector(
        alignments=(
            4,
        )
    )


    result = detector.detect(
        bytes(32),
    )


    assert result[0].alignment == 4
    assert result[0].offset == 0



# ----------------------------------------------------------------------
# Score
# ----------------------------------------------------------------------


def test_score_range() -> None:

    detector = AlignmentDetector()


    result = detector.detect(
        bytes(100),
    )


    for item in result:

        assert 0 <= item.score <= 1



# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------


def test_custom_alignments() -> None:

    detector = AlignmentDetector(
        alignments=(
            16,
        )
    )


    result = detector.detect(
        bytes(64),
    )


    assert result[0].alignment == 16



def test_alignments_property() -> None:

    detector = AlignmentDetector(
        alignments=(
            4,
            8,
        )
    )


    assert detector.alignments == (
        4,
        8,
    )