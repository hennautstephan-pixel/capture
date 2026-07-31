from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from capture_recovery.core.recovered_value import RecoveredValue


def test_recovered_value_creation() -> None:
    value = RecoveredValue(
        type="string",
        value="Robe Esprite",
        offset=100,
        size=12,
    )

    assert value.type == "string"
    assert value.value == "Robe Esprite"
    assert value.offset == 100
    assert value.size == 12
    assert value.confidence == 1.0
    assert value.detector == ""
    assert value.source == ""


def test_end_offset() -> None:
    value = RecoveredValue(type="int", value=42, offset=100, size=12)

    assert value.end_offset == 112


def test_overlap_true() -> None:
    a = RecoveredValue(type="int", value=1, offset=100, size=20)
    b = RecoveredValue(type="int", value=2, offset=110, size=15)

    assert a.overlaps(b) is True
    assert b.overlaps(a) is True


def test_overlap_false() -> None:
    a = RecoveredValue(type="int", value=1, offset=100, size=10)
    b = RecoveredValue(type="int", value=2, offset=120, size=10)

    assert a.overlaps(b) is False
    assert b.overlaps(a) is False


def test_recovered_value_is_frozen() -> None:
    value = RecoveredValue(type="float", value=1.0, offset=0, size=4)

    with pytest.raises(FrozenInstanceError):
        value.offset = 5


def test_zero_length_value() -> None:
    value = RecoveredValue(type="string", value="", offset=100, size=0)

    assert value.end_offset == 100
    assert value.overlaps(RecoveredValue(type="string", value="", offset=100, size=0)) is False
