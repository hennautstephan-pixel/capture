from capture_recovery.memory.memory_index import MemoryIndex
from capture_recovery.memory.memory_map import MemoryMap
from capture_recovery.memory.region import MemoryRegion


def build():

    memory = MemoryMap()

    memory.add(
        MemoryRegion(
            0,
            10,
            "HEADER",
        )
    )

    memory.add(
        MemoryRegion(
            100,
            20,
            "ASCII",
        )
    )

    memory.add(
        MemoryRegion(
            200,
            50,
            "FLOAT",
        )
    )

    return MemoryIndex(memory)


def test_at():

    index = build()

    region = index.at(105)

    assert region is not None
    assert region.kind == "ASCII"


def test_at_missing():

    index = build()

    assert index.at(50) is None


def test_before():

    index = build()

    region = index.before(110)

    assert region is not None
    assert region.kind == "ASCII"


def test_after():

    index = build()

    region = index.after(110)

    assert region is not None
    assert region.kind == "FLOAT"


def test_between():

    index = build()

    regions = index.between(50, 210)

    assert len(regions) == 2


def test_by_kind():

    index = build()

    assert len(index.by_kind("FLOAT")) == 1