"""
Tests for capture_recovery.reverse.offset_iterator.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.detection_options import (
    DetectionOptions,
)

from capture_recovery.reverse.detection_strategy import (
    DetectionStrategy,
)

from capture_recovery.reverse.offset_iterator import (
    OffsetIterator,
)


# ----------------------------------------------------------------------
# SCAN
# ----------------------------------------------------------------------


def test_scan_offsets() -> None:

    options = DetectionOptions()

    result = list(
        OffsetIterator.iterate(
            length=10,
            value_size=4,
            options=options,
        )
    )

    assert result == [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
    ]


def test_scan_with_start() -> None:

    options = DetectionOptions(
        start=3,
    )

    result = OffsetIterator.list_offsets(
        10,
        4,
        options,
    )

    assert result == [
        3,
        4,
        5,
        6,
    ]


# ----------------------------------------------------------------------
# ALIGNED
# ----------------------------------------------------------------------


def test_aligned_offsets() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.ALIGNED,
        alignment=4,
    )

    result = OffsetIterator.list_offsets(
        20,
        4,
        options,
    )

    assert result == [
        0,
        4,
        8,
        12,
        16,
    ]


# ----------------------------------------------------------------------
# CUSTOM
# ----------------------------------------------------------------------


def test_custom_offsets() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.CUSTOM,
        offsets=(20, 5, 10),
    )

    result = OffsetIterator.list_offsets(
        32,
        4,
        options,
    )

    assert result == [
        5,
        10,
        20,
    ]


def test_custom_out_of_range_removed() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.CUSTOM,
        offsets=(1, 100),
    )

    result = OffsetIterator.list_offsets(
        10,
        4,
        options,
    )

    assert result == [
        1,
    ]


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------


def test_negative_length_rejected() -> None:

    with pytest.raises(ValueError):

        list(
            OffsetIterator.iterate(
                -1,
                4,
                DetectionOptions(),
            )
        )


def test_zero_value_size_rejected() -> None:

    with pytest.raises(ValueError):

        list(
            OffsetIterator.iterate(
                10,
                0,
                DetectionOptions(),
            )
        )


# ----------------------------------------------------------------------
# Boundary
# ----------------------------------------------------------------------


def test_exact_size_buffer() -> None:

    result = OffsetIterator.list_offsets(
        4,
        4,
        DetectionOptions(),
    )

    assert result == [
        0,
    ]


def test_too_small_buffer() -> None:

    result = OffsetIterator.list_offsets(
        3,
        4,
        DetectionOptions(),
    )

    assert result == []