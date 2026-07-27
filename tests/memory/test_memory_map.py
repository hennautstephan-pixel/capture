from capture_recovery.memory.memory_map import MemoryMap
from capture_recovery.memory.region import MemoryRegion


def test_empty():

    memory = MemoryMap()

    assert len(memory) == 0


def test_add():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            0,
            10,
            "ASCII",
        )
    )

    assert len(memory) == 1


def test_find():

    memory = MemoryMap()

    region = MemoryRegion(
        100,
        50,
        "ASCII",
    )

    memory.add(region)

    assert memory.find(120) is region


def test_find_missing():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            100,
            20,
            "ASCII",
        )
    )

    assert memory.find(50) is None


def test_by_kind():

    memory = MemoryMap()

    memory.add(MemoryRegion(0, 10, "ASCII"))
    memory.add(MemoryRegion(20, 10, "FLOAT"))

    assert len(memory.by_kind("ASCII")) == 1
    assert len(memory.by_kind("FLOAT")) == 1


def test_merge():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            0,
            10,
            "ASCII",
        )
    )

    memory.add(
        MemoryRegion(
            10,
            15,
            "ASCII",
        )
    )

    memory.merge_adjacent()

    assert len(memory) == 1
    assert memory[0].size == 25


def test_overlap():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            0,
            20,
            "A",
        )
    )

    memory.add(
        MemoryRegion(
            10,
            20,
            "B",
        )
    )

    assert len(memory.overlapping()) == 1


def test_gap():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            100,
            50,
            "A",
        )
    )

    gaps = memory.gaps(200)

    assert gaps == [
        (0, 100),
        (150, 50),
    ]


def test_statistics():

    memory = MemoryMap()

    memory.add(MemoryRegion(0, 10, "ASCII"))
    memory.add(MemoryRegion(20, 20, "ASCII"))
    memory.add(MemoryRegion(100, 5, "FLOAT"))

    stats = memory.statistics()

    assert stats["ASCII"] == 2
    assert stats["FLOAT"] == 1


def test_total_size():

    memory = MemoryMap()

    memory.add(MemoryRegion(0, 10, "A"))
    memory.add(MemoryRegion(20, 30, "B"))

    assert memory.total_size == 40