from capture_recovery.parser import (
    ObjectCollection,
    ObjectParser,
    ParsedObject,
)


def test_empty():

    result = ObjectParser().parse(b"")

    assert result.is_empty

    assert result.count == 0


def test_parse():

    data = b"abcdef"

    result = ObjectParser().parse(data)

    assert isinstance(result, ObjectCollection)

    assert result.count == 1

    obj = result.objects[0]

    assert isinstance(obj, ParsedObject)

    assert obj.offset == 0

    assert obj.size == 6

    assert obj.raw == data


def test_object_empty():

    obj = ParsedObject(
        offset=0,
        size=0,
        raw=b"",
    )

    assert obj.is_empty