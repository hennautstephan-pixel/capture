"""
Tests for public reverse imports.
"""

from __future__ import annotations



def test_import_api():

    from capture_recovery.reverse import analyze

    assert callable(
        analyze
    )



def test_import_engine():

    from capture_recovery.reverse import (
        ReverseEngine,
        ReverseResult,
    )


    assert ReverseEngine is not None
    assert ReverseResult is not None



def test_import_detectors():

    from capture_recovery.reverse import (
        NumericDetector,
        StringDetector,
        GuidDetector,
        AlignmentDetector,
        EntropyDetector,
    )


    assert NumericDetector is not None
    assert StringDetector is not None
    assert GuidDetector is not None
    assert AlignmentDetector is not None
    assert EntropyDetector is not None



def test_import_values():

    from capture_recovery.reverse import (
        NumericValue,
        StringValue,
        GuidValue,
        AlignmentValue,
        EntropyValue,
    )


    assert NumericValue is not None
    assert StringValue is not None
    assert GuidValue is not None
    assert AlignmentValue is not None
    assert EntropyValue is not None



def test_public_analysis():

    from capture_recovery.reverse import analyze


    result = analyze(
        b"Hello\x00"
    )


    assert result is not None