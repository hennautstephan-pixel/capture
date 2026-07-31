from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any, Iterable

import pytest


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from capture_recovery.core.semantic_correlator import SemanticCorrelator, SemanticObject


def test_semantic_object_defaults() -> None:
    obj = SemanticObject(
        object_type="fixture",
        properties={"name": "Test"},
        confidence=1.0,
        source_offsets=(100, 120),
    )

    assert obj.object_type == "fixture"
    assert obj.properties == {"name": "Test"}
    assert obj.confidence == 1.0
    assert obj.source_offsets == (100, 120)


def test_semantic_object_is_frozen() -> None:
    obj = SemanticObject(
        object_type="fixture",
        properties={},
        confidence=0.5,
        source_offsets=(1,),
    )

    with pytest.raises(FrozenInstanceError):
        obj.object_type = "scene"


def test_correlator_returns_empty_list() -> None:
    class DummyCorrelator(SemanticCorrelator):
        def correlate(self, values: Iterable[Any]) -> list[SemanticObject]:
            return super().correlate(values)

    result = DummyCorrelator().correlate([])

    assert result == []


def test_correlator_accepts_iterable() -> None:
    class DummyCorrelator(SemanticCorrelator):
        def correlate(self, values: Iterable[Any]) -> list[SemanticObject]:
            return super().correlate(values)

    result = DummyCorrelator().correlate(["abc", 123, object()])

    assert result == []
