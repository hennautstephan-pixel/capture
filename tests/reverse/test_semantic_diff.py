from __future__ import annotations

import sys
from pathlib import Path

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.reverse.semantic_diff import (
    DiffKind,
    SemanticDiffEngine,
    ValueDifference,
)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_compare_returns_unchanged_for_identical_values() -> None:
    engine = SemanticDiffEngine()
    before = [RecoveredValue(type="int", value=1, offset=10, size=4)]
    after = [RecoveredValue(type="int", value=1, offset=10, size=4)]

    diff = engine.compare(before, after)

    assert diff.added == ()
    assert diff.removed == ()
    assert diff.modified == ()
    assert diff.unchanged == (
        ValueDifference(kind=DiffKind.UNCHANGED, before=before[0], after=after[0]),
    )


def test_compare_detects_added_value() -> None:
    engine = SemanticDiffEngine()
    before = [RecoveredValue(type="int", value=1, offset=10, size=4)]
    after = [
        RecoveredValue(type="int", value=1, offset=10, size=4),
        RecoveredValue(type="string", value="hello", offset=20, size=5),
    ]

    diff = engine.compare(before, after)

    assert diff.added == (
        ValueDifference(kind=DiffKind.ADDED, before=None, after=after[1]),
    )
    assert diff.removed == ()
    assert diff.modified == ()
    assert diff.unchanged == (
        ValueDifference(kind=DiffKind.UNCHANGED, before=before[0], after=after[0]),
    )


def test_compare_detects_removed_value() -> None:
    engine = SemanticDiffEngine()
    before = [
        RecoveredValue(type="int", value=1, offset=10, size=4),
        RecoveredValue(type="string", value="hello", offset=20, size=5),
    ]
    after = [RecoveredValue(type="int", value=1, offset=10, size=4)]

    diff = engine.compare(before, after)

    assert diff.added == ()
    assert diff.removed == (
        ValueDifference(kind=DiffKind.REMOVED, before=before[1], after=None),
    )
    assert diff.modified == ()
    assert diff.unchanged == (
        ValueDifference(kind=DiffKind.UNCHANGED, before=before[0], after=after[0]),
    )


def test_compare_detects_modified_value() -> None:
    engine = SemanticDiffEngine()
    before = [RecoveredValue(type="int", value=1, offset=10, size=4)]
    after = [RecoveredValue(type="int", value=2, offset=10, size=4)]

    diff = engine.compare(before, after)

    assert diff.added == ()
    assert diff.removed == ()
    assert diff.modified == (
        ValueDifference(kind=DiffKind.MODIFIED, before=before[0], after=after[0]),
    )
    assert diff.unchanged == ()


def test_compare_handles_multiple_differences() -> None:
    engine = SemanticDiffEngine()
    before = [
        RecoveredValue(type="int", value=1, offset=10, size=4),
        RecoveredValue(type="string", value="old", offset=30, size=3),
    ]
    after = [
        RecoveredValue(type="int", value=2, offset=10, size=4),
        RecoveredValue(type="string", value="old", offset=30, size=3),
        RecoveredValue(type="float", value=1.5, offset=50, size=8),
    ]

    diff = engine.compare(before, after)

    assert diff.added == (
        ValueDifference(kind=DiffKind.ADDED, before=None, after=after[2]),
    )
    assert diff.removed == ()
    assert diff.modified == (
        ValueDifference(kind=DiffKind.MODIFIED, before=before[0], after=after[0]),
    )
    assert diff.unchanged == (
        ValueDifference(kind=DiffKind.UNCHANGED, before=before[1], after=after[1]),
    )


def test_compare_is_order_insensitive_when_keys_match() -> None:
    engine = SemanticDiffEngine()
    before = [
        RecoveredValue(type="int", value=1, offset=10, size=4),
        RecoveredValue(type="string", value="hello", offset=20, size=5),
    ]
    after = [
        RecoveredValue(type="string", value="hello", offset=20, size=5),
        RecoveredValue(type="int", value=1, offset=10, size=4),
    ]

    diff = engine.compare(before, after)

    assert diff.added == ()
    assert diff.removed == ()
    assert diff.modified == ()
    assert len(diff.unchanged) == 2


def test_compare_handles_empty_iterables() -> None:
    engine = SemanticDiffEngine()

    diff = engine.compare([], [])

    assert diff.added == ()
    assert diff.removed == ()
    assert diff.modified == ()
    assert diff.unchanged == ()
