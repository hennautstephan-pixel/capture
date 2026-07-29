"""
Tests for capture_recovery.reverse.pattern_detector
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.pattern_detector import (
    Pattern,
    PatternDetector,
)


def test_empty_buffer():
    assert PatternDetector.detect(b"") == []


def test_invalid_pattern_size():
    with pytest.raises(ValueError):
        PatternDetector.detect(b"abc", pattern_size=0)


def test_invalid_min_occurrences():
    with pytest.raises(ValueError):
        PatternDetector.detect(
            b"abc",
            min_occurrences=1,
        )


def test_invalid_step():
    with pytest.raises(ValueError):
        PatternDetector.detect(
            b"abc",
            step=0,
        )


def test_detect_single_pattern():
    data = b"ABCD1234ABCD"

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert len(patterns) == 1

    p = patterns[0]

    assert p.data == b"ABCD"
    assert p.length == 4
    assert p.offsets == (0, 8)
    assert p.count == 2


def test_no_pattern():
    data = b"ABCDEFGH"

    assert PatternDetector.detect(
        data,
        pattern_size=4,
    ) == []


def test_multiple_occurrences():
    data = b"AAAAxxxxAAAAyyyyAAAA"

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert patterns[0].count == 3
    assert patterns[0].offsets == (
        0,
        8,
        16,
    )


def test_memoryview_supported():
    data = memoryview(
        b"ABCDxxxxABCD"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert len(patterns) == 1


def test_bytearray_supported():
    data = bytearray(
        b"ABCDxxxxABCD"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert len(patterns) == 1


def test_step_four():
    data = (
        b"ABCD"
        b"EFGH"
        b"ABCD"
        b"IJKL"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
        step=4,
    )

    assert patterns[0].offsets == (
        0,
        8,
    )


def test_histogram():
    patterns = PatternDetector.detect(
        b"ABCDxxxxABCD",
        pattern_size=4,
    )

    hist = PatternDetector.histogram(
        patterns
    )

    assert hist == {4: 1}


def test_largest():
    patterns = PatternDetector.detect(
        b"ABCDxxxxABCD",
        pattern_size=4,
    )

    largest = PatternDetector.largest(
        patterns,
        1,
    )

    assert len(largest) == 1
    assert largest[0].length == 4


def test_most_frequent():
    patterns = PatternDetector.detect(
        b"ABCDxxxxABCD",
        pattern_size=4,
    )

    freq = PatternDetector.most_frequent(
        patterns,
        1,
    )

    assert len(freq) == 1
    assert freq[0].count == 2


def test_pattern_is_hashable():
    p = Pattern(
        data=b"ABCD",
        length=4,
        offsets=(0, 8),
    )

    assert hash(p)


def test_pattern_count_property():
    p = Pattern(
        data=b"AA",
        length=2,
        offsets=(1, 5, 9),
    )

    assert p.count == 3


def test_detect_three_patterns():
    data = (
        b"AAAA"
        b"BBBB"
        b"AAAA"
        b"CCCC"
        b"BBBB"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert len(patterns) == 2


def test_min_occurrences_three():
    data = (
        b"ABCD"
        b"xxxx"
        b"ABCD"
        b"yyyy"
        b"ABCD"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
        min_occurrences=3,
    )

    assert len(patterns) == 1
    assert patterns[0].count == 3


def test_sort_order():
    data = (
        b"ABCD"
        b"xxxx"
        b"ABCD"
        b"yyyy"
        b"ABCD"
    )

    patterns = PatternDetector.detect(
        data,
        pattern_size=4,
    )

    assert patterns == sorted(
        patterns,
        key=lambda p: (
            -p.length,
            -p.count,
            p.offsets[0],
        ),
    )


def test_no_false_positive_with_short_buffer():
    assert PatternDetector.detect(
        b"ABC",
        pattern_size=4,
    ) == []


def test_histogram_empty():
    assert (
        PatternDetector.histogram([])
        == {}
    )


def test_largest_empty():
    assert (
        PatternDetector.largest([])
        == []
    )


def test_most_frequent_empty():
    assert (
        PatternDetector.most_frequent([])
        == []
    )