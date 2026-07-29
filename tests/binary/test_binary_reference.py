from dataclasses import FrozenInstanceError

import pytest

from capture_recovery.binary.binary_reference import BinaryReference


def test_binary_reference_creation() -> None:
    ref = BinaryReference(
        source=10,
        target=20,
        offset=128,
    )

    assert ref.source == 10
    assert ref.target == 20
    assert ref.offset == 128
    assert ref.kind == "pointer"


def test_custom_kind() -> None:
    ref = BinaryReference(
        source=1,
        target=2,
        offset=5,
        kind="owner",
    )

    assert ref.kind == "owner"


def test_equality() -> None:
    ref1 = BinaryReference(
        source=1,
        target=2,
        offset=3,
    )

    ref2 = BinaryReference(
        source=1,
        target=2,
        offset=3,
    )

    assert ref1 == ref2


def test_hashable() -> None:
    ref = BinaryReference(
        source=1,
        target=2,
        offset=10,
    )

    mapping = {ref: "ok"}

    assert mapping[ref] == "ok"


def test_is_frozen() -> None:
    ref = BinaryReference(
        source=1,
        target=2,
        offset=3,
    )

    with pytest.raises(FrozenInstanceError):
        ref.source = 99  # type: ignore[misc]


def test_slots() -> None:
    ref = BinaryReference(
        source=1,
        target=2,
        offset=3,
    )

    with pytest.raises(AttributeError):
        ref.new_attribute = "invalid"  # type: ignore[attr-defined]


def test_zero_offset() -> None:
    ref = BinaryReference(
        source=100,
        target=200,
        offset=0,
    )

    assert ref.offset == 0


def test_negative_identifier_allowed() -> None:
    """
    The binary model does not enforce semantic validation.
    """

    ref = BinaryReference(
        source=-1,
        target=-2,
        offset=0,
    )

    assert ref.source == -1
    assert ref.target == -2