"""
Tests for entropy_value.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.entropy_value import (
    EntropyValue,
)



def create_value():

    return EntropyValue(
        offset=0,
        entropy=7.5,
        length=256,
        score=0.93,
    )



def test_create_entropy_value():

    value = create_value()

    assert value.entropy == 7.5
    assert value.length == 256



def test_end_offset():

    value = create_value()

    assert value.end_offset == 256



def test_high_entropy():

    value = create_value()

    assert value.is_high_entropy is True



def test_low_entropy():

    value = EntropyValue(
        offset=0,
        entropy=2,
        length=10,
        score=0.2,
    )

    assert value.is_high_entropy is False



def test_invalid_entropy():

    with pytest.raises(ValueError):

        EntropyValue(
            offset=0,
            entropy=9,
            length=10,
            score=0.5,
        )



def test_invalid_score():

    with pytest.raises(ValueError):

        EntropyValue(
            offset=0,
            entropy=5,
            length=10,
            score=2,
        )



def test_invalid_offset():

    with pytest.raises(ValueError):

        EntropyValue(
            offset=-1,
            entropy=5,
            length=10,
            score=0.5,
        )



def test_as_dict():

    value = create_value()

    result = value.as_dict()

    assert result["entropy"] == 7.5