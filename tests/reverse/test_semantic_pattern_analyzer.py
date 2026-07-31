from __future__ import annotations

import sys
from pathlib import Path

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.reverse.semantic_diff import DiffKind, SemanticDiff, ValueDifference
from capture_recovery.reverse.semantic_pattern_analyzer import PatternObservation, SemanticPatternAnalyzer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def test_analyze_returns_empty_report_for_no_diffs() -> None:
    analyzer = SemanticPatternAnalyzer()

    report = analyzer.analyze([])

    assert report.observations == ()
    assert report.statistics["semantic_diff_count"] == 0
    assert report.statistics["total_changed_values"] == 0
    assert report.statistics["unique_offsets"] == 0
    assert report.statistics["detected_groups"] == 0
    assert report.statistics["diff_kind_frequency"] == {
        "ADDED": 0,
        "REMOVED": 0,
        "MODIFIED": 0,
        "UNCHANGED": 0,
    }


def test_analyze_single_diff() -> None:
    analyzer = SemanticPatternAnalyzer()
    diff = SemanticDiff(
        added=(ValueDifference(kind=DiffKind.ADDED, after=RecoveredValue(type="string", value="A", offset=10, size=1)),),
        removed=(),
        modified=(),
        unchanged=(),
    )

    report = analyzer.analyze([diff])

    assert report.statistics["semantic_diff_count"] == 1
    assert report.statistics["total_changed_values"] == 1
    assert report.statistics["unique_offsets"] == 1
    assert report.statistics["detected_groups"] == 0
    assert report.statistics["diff_kind_frequency"]["ADDED"] == 1


def test_analyze_multiple_identical_diffs() -> None:
    analyzer = SemanticPatternAnalyzer()
    diff = SemanticDiff(
        added=(ValueDifference(kind=DiffKind.ADDED, after=RecoveredValue(type="string", value="A", offset=10, size=1)),),
        removed=(),
        modified=(),
        unchanged=(),
    )

    report = analyzer.analyze([diff, diff])

    assert report.statistics["total_changed_values"] == 2
    assert report.statistics["detected_groups"] == 0
    assert any(observation.pattern_id == "type_string" for observation in report.observations)


def test_analyze_multiple_different_diffs() -> None:
    analyzer = SemanticPatternAnalyzer()
    first = SemanticDiff(
        added=(ValueDifference(kind=DiffKind.ADDED, after=RecoveredValue(type="string", value="A", offset=10, size=1)),),
        removed=(),
        modified=(),
        unchanged=(),
    )
    second = SemanticDiff(
        added=(),
        removed=(),
        modified=(ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=1, offset=20, size=4), after=RecoveredValue(type="int", value=2, offset=20, size=4)),),
        unchanged=(),
    )

    report = analyzer.analyze([first, second])

    assert report.statistics["total_changed_values"] == 2
    assert report.statistics["diff_kind_frequency"]["ADDED"] == 1
    assert report.statistics["diff_kind_frequency"]["MODIFIED"] == 1


def test_analyze_groups_recurrent_offsets() -> None:
    analyzer = SemanticPatternAnalyzer()
    diff_one = SemanticDiff(
        added=(),
        removed=(),
        modified=(
            ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=1, offset=5, size=4), after=RecoveredValue(type="int", value=2, offset=5, size=4)),
            ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=3, offset=6, size=4), after=RecoveredValue(type="int", value=4, offset=6, size=4)),
        ),
        unchanged=(),
    )
    diff_two = SemanticDiff(
        added=(),
        removed=(),
        modified=(
            ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=5, offset=5, size=4), after=RecoveredValue(type="int", value=6, offset=5, size=4)),
        ),
        unchanged=(),
    )

    report = analyzer.analyze([diff_one, diff_two])

    offset_group_observation = next(observation for observation in report.observations if observation.pattern_id.startswith("offset_group_"))
    assert offset_group_observation.offsets == (5, 6)
    assert offset_group_observation.occurrences == 1


def test_analyze_calculates_statistics() -> None:
    analyzer = SemanticPatternAnalyzer()
    diff = SemanticDiff(
        added=(ValueDifference(kind=DiffKind.ADDED, after=RecoveredValue(type="string", value="A", offset=10, size=1)),),
        removed=(ValueDifference(kind=DiffKind.REMOVED, before=RecoveredValue(type="uuid", value="u", offset=11, size=16)),),
        modified=(ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=1, offset=12, size=4), after=RecoveredValue(type="int", value=2, offset=12, size=4)),),
        unchanged=(),
    )

    report = analyzer.analyze([diff])

    assert report.statistics["total_changed_values"] == 3
    assert report.statistics["unique_offsets"] == 3
    assert report.statistics["value_type_frequency"] == {"string": 1, "uuid": 1, "int": 1}


def test_analyze_is_stable_regardless_of_input_order() -> None:
    analyzer = SemanticPatternAnalyzer()
    first = SemanticDiff(
        added=(ValueDifference(kind=DiffKind.ADDED, after=RecoveredValue(type="string", value="A", offset=10, size=1)),),
        removed=(),
        modified=(),
        unchanged=(),
    )
    second = SemanticDiff(
        added=(),
        removed=(),
        modified=(ValueDifference(kind=DiffKind.MODIFIED, before=RecoveredValue(type="int", value=1, offset=20, size=4), after=RecoveredValue(type="int", value=2, offset=20, size=4)),),
        unchanged=(),
    )

    first_report = analyzer.analyze([first, second])
    second_report = analyzer.analyze([second, first])

    assert first_report.statistics == second_report.statistics
    assert first_report.observations == second_report.observations
