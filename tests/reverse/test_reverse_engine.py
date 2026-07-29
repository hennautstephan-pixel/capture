"""
Tests for reverse_engine.
"""

from __future__ import annotations


from capture_recovery.reverse.reverse_engine import (
    ReverseEngine,
)



def test_engine_creation():

    engine = ReverseEngine()

    assert engine is not None



def test_engine_analyze_empty():

    engine = ReverseEngine()

    result = engine.analyze(
        b"",
    )


    assert result.total >= 0



def test_engine_detect_string():

    engine = ReverseEngine()


    result = engine.analyze(
        b"Hello World\x00",
    )


    assert any(
        item.value == "Hello World"
        for item in result.strings
    )



def test_engine_detect_guid():

    engine = ReverseEngine()


    data = bytes.fromhex(
        "78563412"
        "3412"
        "cdab"
        "ef0123456789abcd"
    )


    result = engine.analyze(
        data,
    )


    assert len(
        result.guids
    ) >= 1



def test_result_total():

    engine = ReverseEngine()

    result = engine.analyze(
        b"test\x00",
    )


    assert result.total >= 0