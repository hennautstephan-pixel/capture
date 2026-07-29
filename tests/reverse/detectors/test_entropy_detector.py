"""
Tests for entropy_detector.
"""

from __future__ import annotations


from capture_recovery.reverse.entropy_detector import (
    EntropyDetector,
)



# ----------------------------------------------------------------------
# Entropy calculation
# ----------------------------------------------------------------------


def test_empty_entropy():

    assert (
        EntropyDetector.calculate_entropy(
            b"",
        )
        ==
        0
    )



def test_constant_entropy():

    value = EntropyDetector.calculate_entropy(
        b"\x00" * 256
    )


    assert value == 0



def test_random_entropy():

    data = bytes(
        range(256)
    )


    value = EntropyDetector.calculate_entropy(
        data
    )


    assert value > 7



# ----------------------------------------------------------------------
# Detection
# ----------------------------------------------------------------------


def test_detect_high_entropy():

    detector = EntropyDetector(
        block_size=256,
    )


    data = bytes(
        range(256)
    )


    result = detector.detect(
        data,
        minimum_entropy=7,
    )


    assert len(result) == 1



def test_no_detection_low_entropy():

    detector = EntropyDetector(
        block_size=256,
    )


    result = detector.detect(
        b"\x00" * 256,
    )


    assert result == []



# ----------------------------------------------------------------------
# API
# ----------------------------------------------------------------------


def test_block_size_property():

    detector = EntropyDetector(
        block_size=128,
    )


    assert detector.block_size == 128