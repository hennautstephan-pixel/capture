from __future__ import annotations

from capture_recovery.diff.models import BinaryChange
from capture_recovery.diff.models import ChangeType
from capture_recovery.diff.region_differ import RegionDiffer
from capture_recovery.memory.memory_map import MemoryMap
from capture_recovery.memory.region import MemoryRegion


def test_empty():
    differ = RegionDiffer()

    memory = MemoryMap()

    result = differ.compare((), memory)

    assert result == ()


def test_one_region_one_change():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    changes = (
        BinaryChange(offset=10),
    )

    result = RegionDiffer().compare(
        changes,
        memory,
    )

    assert len(result) == 1

    assert result[0].region is region

    assert len(result[0].binary_changes) == 1

    assert result[0].binary_changes[0].offset == 10


def test_multiple_changes_same_region():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    changes = (
        BinaryChange(offset=30),
        BinaryChange(offset=10),
        BinaryChange(offset=20),
    )

    result = RegionDiffer().compare(
        changes,
        memory,
    )

    assert len(result) == 1

    offsets = [
        c.offset
        for c in result[0].binary_changes
    ]

    assert offsets == [10, 20, 30]


def test_multiple_regions():

    memory = MemoryMap()

    header = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    fixtures = MemoryRegion(
        offset=100,
        size=100,
        kind="fixtures",
    )

    memory.add(header)
    memory.add(fixtures)

    changes = (
        BinaryChange(offset=10),
        BinaryChange(offset=120),
        BinaryChange(offset=150),
    )

    result = RegionDiffer().compare(
        changes,
        memory,
    )

    assert len(result) == 2

    assert result[0].region is header

    assert result[1].region is fixtures

    assert len(result[0].binary_changes) == 1

    assert len(result[1].binary_changes) == 2


def test_change_outside_regions():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            offset=0,
            size=50,
            kind="header",
        )
    )

    changes = (
        BinaryChange(offset=300),
    )

    result = RegionDiffer().compare(
        changes,
        memory,
    )

    assert result == ()


def test_region_order():

    memory = MemoryMap()

    second = MemoryRegion(
        offset=100,
        size=100,
        kind="second",
    )

    first = MemoryRegion(
        offset=0,
        size=50,
        kind="first",
    )

    memory.add(second)
    memory.add(first)

    changes = (
        BinaryChange(offset=120),
        BinaryChange(offset=20),
    )

    result = RegionDiffer().compare(
        changes,
        memory,
    )

    assert len(result) == 2

    assert result[0].offset == 0

    assert result[1].offset == 100


def test_compare_report():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    changes = (
        BinaryChange(offset=20),
    )

    differ = RegionDiffer()

    report = differ.compare_report(
        changes,
        memory,
    )

    assert report == differ.compare(
        changes,
        memory,
    )


def test_preserve_change():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    change = BinaryChange(
        offset=10,
        before=b"A",
        after=b"B",
        change_type=ChangeType.MODIFY,
        confidence=0.75,
    )

    result = RegionDiffer().compare(
        (change,),
        memory,
    )

    returned = result[0].binary_changes[0]

    assert returned.before == b"A"
    assert returned.after == b"B"
    assert returned.change_type is ChangeType.MODIFY
    assert returned.confidence == 0.75


def test_binary_changes_are_tuple():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    result = RegionDiffer().compare(
        (BinaryChange(offset=5),),
        memory,
    )

    assert isinstance(
        result[0].binary_changes,
        tuple,
    )


def test_result_is_tuple():

    memory = MemoryMap()

    region = MemoryRegion(
        offset=0,
        size=100,
        kind="header",
    )

    memory.add(region)

    result = RegionDiffer().compare(
        (BinaryChange(offset=5),),
        memory,
    )

    assert isinstance(result, tuple)