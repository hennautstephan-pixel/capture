"""
Tests for capture_recovery.reverse.detection_options.
"""

from __future__ import annotations

import pytest

from capture_recovery.reverse.detection_options import (
    DetectionOptions,
)

from capture_recovery.reverse.detection_strategy import (
    DetectionStrategy,
)

from capture_recovery.reverse.detector_type import (
    DetectorType,
)


# ----------------------------------------------------------------------
# Defaults
# ----------------------------------------------------------------------


def test_default_values() -> None:

    options = DetectionOptions()

    assert options.strategy is DetectionStrategy.SCAN
    assert options.start == 0
    assert options.stop is None
    assert options.alignment == 1
    assert options.offsets == ()
    assert options.finite_only is True
    assert options.enabled_types is None


# ----------------------------------------------------------------------
# Range validation
# ----------------------------------------------------------------------


def test_negative_start_rejected() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            start=-1,
        )


def test_stop_before_start_rejected() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            start=100,
            stop=50,
        )


def test_equal_start_stop_allowed() -> None:

    options = DetectionOptions(
        start=10,
        stop=10,
    )

    assert options.stop == 10


# ----------------------------------------------------------------------
# Alignment validation
# ----------------------------------------------------------------------


def test_zero_alignment_rejected() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            alignment=0,
        )


def test_negative_alignment_rejected() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            alignment=-4,
        )


def test_positive_alignment_allowed() -> None:

    options = DetectionOptions(
        alignment=8,
    )

    assert options.alignment == 8


# ----------------------------------------------------------------------
# Custom offsets
# ----------------------------------------------------------------------


def test_custom_strategy_requires_offsets() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            strategy=DetectionStrategy.CUSTOM,
        )


def test_custom_strategy_accepts_offsets() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.CUSTOM,
        offsets=(10, 20, 30),
    )

    assert options.offsets == (
        10,
        20,
        30,
    )


def test_offsets_negative_rejected() -> None:

    with pytest.raises(ValueError):

        DetectionOptions(
            offsets=(-1, 5),
        )


# ----------------------------------------------------------------------
# Offset normalization
# ----------------------------------------------------------------------


def test_offsets_are_sorted() -> None:

    options = DetectionOptions(
        offsets=(
            30,
            10,
            20,
        )
    )

    assert options.offsets == (
        10,
        20,
        30,
    )


def test_offsets_duplicates_removed() -> None:

    options = DetectionOptions(
        offsets=(
            10,
            20,
            10,
            30,
            20,
        )
    )

    assert options.offsets == (
        10,
        20,
        30,
    )


def test_offsets_are_tuple() -> None:

    options = DetectionOptions(
        offsets=[5, 2, 1],
    )

    assert isinstance(
        options.offsets,
        tuple,
    )


# ----------------------------------------------------------------------
# Detector types
# ----------------------------------------------------------------------


def test_enabled_types_normalized() -> None:

    options = DetectionOptions(
        enabled_types={
            DetectorType.NUMERIC,
            DetectorType.STRING,
        },
    )

    assert isinstance(
        options.enabled_types,
        frozenset,
    )


def test_allows_type_without_filter() -> None:

    options = DetectionOptions()

    assert options.allows_type(
        DetectorType.NUMERIC
    )


def test_allows_enabled_type() -> None:

    options = DetectionOptions(
        enabled_types={
            DetectorType.NUMERIC,
        }
    )

    assert options.allows_type(
        DetectorType.NUMERIC
    )


def test_rejects_disabled_type() -> None:

    options = DetectionOptions(
        enabled_types={
            DetectorType.NUMERIC,
        }
    )

    assert not options.allows_type(
        DetectorType.STRING
    )


# ----------------------------------------------------------------------
# has_custom_offsets
# ----------------------------------------------------------------------


def test_has_custom_offsets_false() -> None:

    options = DetectionOptions()

    assert not options.has_custom_offsets()


def test_has_custom_offsets_true() -> None:

    options = DetectionOptions(
        offsets=(10,),
    )

    assert options.has_custom_offsets()


# ----------------------------------------------------------------------
# Frozen dataclass
# ----------------------------------------------------------------------


def test_options_are_immutable() -> None:

    options = DetectionOptions()

    with pytest.raises(
        AttributeError
    ):

        options.start = 10


def test_unknown_attribute_rejected() -> None:

    options = DetectionOptions()

    with pytest.raises(
        AttributeError
    ):

        options.new_value = 123


# ----------------------------------------------------------------------
# Strategy compatibility
# ----------------------------------------------------------------------


def test_scan_strategy_default() -> None:

    options = DetectionOptions()

    assert options.strategy is DetectionStrategy.SCAN


def test_aligned_strategy() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.ALIGNED,
        alignment=4,
    )

    assert options.strategy is DetectionStrategy.ALIGNED


def test_custom_strategy() -> None:

    options = DetectionOptions(
        strategy=DetectionStrategy.CUSTOM,
        offsets=(1, 2),
    )

    assert options.strategy is DetectionStrategy.CUSTOM