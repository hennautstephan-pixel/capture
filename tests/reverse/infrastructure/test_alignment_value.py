"""
Tests for alignment_value.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.alignment_value import (
    AlignmentValue,
)



def create_value():

    return AlignmentValue(
        offset=8,
        alignment=4,
        score=0.95,
        length=64,
    )



def test_create_alignment_value():

    value = create_value()

    assert value.offset == 8
    assert value.alignment == 4



def test_end_offset():

    value = create_value()

    assert value.end_offset == 72



def test_is_aligned():

    value = create_value()

    assert value.is_aligned is True



def test_invalid_offset():

    with pytest.raises(ValueError):

        AlignmentValue(
            offset=-1,
            alignment=4,
            score=1,
            length=10,
        )



def test_invalid_alignment():

    with pytest.raises(ValueError):

        AlignmentValue(
            offset=0,
            alignment=0,
            score=1,
            length=10,
        )



def test_invalid_score_high():

    with pytest.raises(ValueError):

        AlignmentValue(
            offset=0,
            alignment=4,
            score=2,
            length=10,
        )



def test_invalid_score_low():

    with pytest.raises(ValueError):

        AlignmentValue(
            offset=0,
            alignment=4,
            score=-1,
            length=10,
        )



def test_as_dict():

    value = create_value()

    result = value.as_dict()

    assert result["alignment"] == 4
    assert result["score"] == 0.95