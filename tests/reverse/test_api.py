"""
Tests for reverse public API.
"""

from __future__ import annotations


from capture_recovery.reverse.api import (
    analyze,
    get_engine,
)

from capture_recovery.reverse.reverse_engine import (
    ReverseEngine,
)



def test_analyze_returns_result():

    result = analyze(
        b"Hello World\x00",
    )


    assert result is not None



def test_analyze_string():

    result = analyze(
        b"Hello World\x00",
    )


    assert any(
        item.value == "Hello World"
        for item in result.strings
    )



def test_analyze_guid():

    data = bytes.fromhex(
        "78563412"
        "3412"
        "cdab"
        "ef0123456789abcd"
    )


    result = analyze(
        data,
    )


    assert len(
        result.guids
    ) >= 1



def test_get_engine():

    engine = get_engine()


    assert isinstance(
        engine,
        ReverseEngine,
    )



def test_same_engine_instance():

    assert (
        get_engine()
        is
        get_engine()
    )