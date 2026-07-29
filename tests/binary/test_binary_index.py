from capture_recovery.binary.binary_index import BinaryIndex
from capture_recovery.binary.binary_object import BinaryObject


def make_object(
    identifier: int,
    offset: int = 0,
    size: int = 1,
) -> BinaryObject:
    return BinaryObject(
        identifier=identifier,
        offset=offset,
        size=size,
        raw_data=b"\x00" * size,
    )


def test_empty_index() -> None:
    index = BinaryIndex(objects={})

    assert index.count() == 0
    assert list(index.all()) == []


def test_get_existing_object() -> None:
    obj = make_object(42)

    index = BinaryIndex(
        objects={
            obj.identifier: obj,
        }
    )

    assert index.get(42) is obj


def test_get_unknown_object() -> None:
    index = BinaryIndex(objects={})

    assert index.get(9999) is None


def test_count() -> None:
    objects = {
        i: make_object(i)
        for i in range(10)
    }

    index = BinaryIndex(objects=objects)

    assert index.count() == 10


def test_all_returns_every_object() -> None:
    objects = {
        1: make_object(1),
        2: make_object(2),
        3: make_object(3),
    }

    index = BinaryIndex(objects=objects)

    identifiers = {
        obj.identifier
        for obj in index.all()
    }

    assert identifiers == {1, 2, 3}


def test_same_instance_is_returned() -> None:
    obj = make_object(5)

    index = BinaryIndex(
        objects={
            5: obj,
        }
    )

    assert index.get(5) is obj


def test_all_returns_values_view() -> None:
    index = BinaryIndex(
        objects={
            1: make_object(1),
        }
    )

    values = index.all()

    assert hasattr(values, "__iter__")
    assert len(list(values)) == 1


def test_large_index() -> None:
    objects = {
        i: make_object(i)
        for i in range(1000)
    }

    index = BinaryIndex(objects=objects)

    assert index.count() == 1000

    assert index.get(999).identifier == 999