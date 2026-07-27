from capture_recovery.memory.region import MemoryRegion


def test_end():

    region = MemoryRegion(
        offset=100,
        size=20,
        kind="ASCII",
    )

    assert region.end == 120


def test_contains():

    region = MemoryRegion(
        offset=10,
        size=10,
        kind="ASCII",
    )

    assert region.contains(10)
    assert region.contains(19)

    assert not region.contains(20)


def test_in_operator():

    region = MemoryRegion(
        offset=10,
        size=10,
        kind="ASCII",
    )

    assert 15 in region
    assert 25 not in region


def test_overlap():

    a = MemoryRegion(0, 20, "A")
    b = MemoryRegion(10, 20, "B")

    assert a.overlaps(b)


def test_no_overlap():

    a = MemoryRegion(0, 10, "A")
    b = MemoryRegion(10, 10, "B")

    assert not a.overlaps(b)


def test_adjacent():

    a = MemoryRegion(0, 10, "A")
    b = MemoryRegion(10, 5, "A")

    assert a.adjacent(b)


def test_merge():

    a = MemoryRegion(
        offset=0,
        size=10,
        kind="ASCII",
        confidence=0.8,
    )

    b = MemoryRegion(
        offset=10,
        size=20,
        kind="ASCII",
        confidence=0.9,
    )

    merged = a.merge(b)

    assert merged.offset == 0
    assert merged.size == 30
    assert merged.confidence == 0.9


def test_len():

    region = MemoryRegion(
        offset=0,
        size=123,
        kind="ASCII",
    )

    assert len(region) == 123


def test_sort():

    a = MemoryRegion(100, 10, "A")
    b = MemoryRegion(10, 10, "A")

    regions = sorted([a, b])

    assert regions[0].offset == 10