from capture_recovery.structures import Field
from capture_recovery.structures import Structure
from capture_recovery.structures import StructureIndex
from capture_recovery.models import DataType


def build():

    a = Structure(
        name="Header",
        offset=0,
        length=16,
    )

    b = Structure(
        name="Fixture",
        offset=100,
        length=32,
    )

    c = Structure(
        name="Fixture",
        offset=200,
        length=32,
    )

    return StructureIndex(
        [
            c,
            a,
            b,
        ]
    )


def test_at():

    index = build()

    assert len(index.at(100)) == 1


def test_before():

    index = build()

    assert len(index.before(150)) == 2


def test_after():

    index = build()

    assert len(index.after(100)) == 1


def test_between():

    index = build()

    assert len(index.between(50, 150)) == 1


def test_overlapping():

    index = build()

    result = index.overlapping(
        110,
        120,
    )

    assert len(result) == 1


def test_by_name():

    index = build()

    assert len(index.by_name("Fixture")) == 2


def test_first():

    index = build()

    assert index.first().offset == 0


def test_last():

    index = build()

    assert index.last().offset == 200