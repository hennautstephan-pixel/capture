from __future__ import annotations

from capture_recovery.diff.binary_differ import BinaryDiffer
from capture_recovery.diff.models import ChangeType


def test_empty_buffers():
    differ = BinaryDiffer()

    result = differ.compare(b"", b"")

    assert result == ()


def test_identical_buffers():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"abcdef",
    )

    assert result == ()


def test_single_modify():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"abcxef",
    )

    assert len(result) == 1

    change = result[0]

    assert change.offset == 3
    assert change.before == b"d"
    assert change.after == b"x"
    assert change.change_type is ChangeType.MODIFY


def test_multiple_modify():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"xbcyez",
    )

    assert len(result) == 3

    assert result[0].offset == 0
    assert result[0].change_type is ChangeType.MODIFY

    assert result[1].offset == 3
    assert result[1].change_type is ChangeType.MODIFY

    assert result[2].offset == 5
    assert result[2].change_type is ChangeType.MODIFY


def test_insert_end():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abc",
        b"abcd",
    )

    assert len(result) == 1

    change = result[0]

    assert change.change_type is ChangeType.INSERT
    assert change.offset == 3
    assert change.before == b""
    assert change.after == b"d"


def test_insert_middle():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"abcXYZdef",
    )

    inserts = [
        c for c in result
        if c.change_type is ChangeType.INSERT
    ]

    assert len(inserts) == 3

    assert inserts[0].after == b"X"
    assert inserts[1].after == b"Y"
    assert inserts[2].after == b"Z"


def test_insert_beginning():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"123abcdef",
    )

    inserts = [
        c for c in result
        if c.change_type is ChangeType.INSERT
    ]

    assert len(inserts) == 3

    assert inserts[0].after == b"1"
    assert inserts[1].after == b"2"
    assert inserts[2].after == b"3"


def test_delete_end():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcd",
        b"abc",
    )

    assert len(result) == 1

    change = result[0]

    assert change.change_type is ChangeType.DELETE
    assert change.offset == 3
    assert change.before == b"d"
    assert change.after == b""


def test_delete_middle():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcXYZdef",
        b"abcdef",
    )

    deletes = [
        c for c in result
        if c.change_type is ChangeType.DELETE
    ]

    assert len(deletes) == 3

    assert deletes[0].before == b"X"
    assert deletes[1].before == b"Y"
    assert deletes[2].before == b"Z"


def test_delete_beginning():
    differ = BinaryDiffer()

    result = differ.compare(
        b"123abcdef",
        b"abcdef",
    )

    deletes = [
        c for c in result
        if c.change_type is ChangeType.DELETE
    ]

    assert len(deletes) == 3

    assert deletes[0].before == b"1"
    assert deletes[1].before == b"2"
    assert deletes[2].before == b"3"


def test_replace_longer():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abc",
        b"abcdef",
    )

    assert len(result) == 3

    assert result[0].change_type is ChangeType.INSERT
    assert result[1].change_type is ChangeType.INSERT
    assert result[2].change_type is ChangeType.INSERT


def test_replace_shorter():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdef",
        b"abc",
    )

    assert len(result) == 3

    assert result[0].change_type is ChangeType.DELETE
    assert result[1].change_type is ChangeType.DELETE
    assert result[2].change_type is ChangeType.DELETE


def test_compare_files(tmp_path):
    before = tmp_path / "before.bin"
    after = tmp_path / "after.bin"

    before.write_bytes(b"abcdef")
    after.write_bytes(b"abcxef")

    differ = BinaryDiffer()

    result = differ.compare_files(
        str(before),
        str(after),
    )

    assert len(result) == 1

    assert result[0].change_type is ChangeType.MODIFY
    assert result[0].offset == 3


def test_result_is_tuple():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abc",
        b"adc",
    )

    assert isinstance(result, tuple)


def test_changes_are_sorted():
    differ = BinaryDiffer()

    result = differ.compare(
        b"abcdefgh",
        b"abXYefZgh",
    )

    offsets = [change.offset for change in result]

    assert offsets == sorted(offsets)