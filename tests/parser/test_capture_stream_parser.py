from capture_recovery.parser import (
    CaptureStream,
    StreamParser,
)


def test_empty():

    stream = StreamParser().parse(b"")

    assert stream.is_empty

    assert stream.section_count == 0


def test_parse():

    data = b"abcdef"

    stream = StreamParser().parse(data)

    assert isinstance(
        stream,
        CaptureStream,
    )

    assert stream.size == 6

    assert stream.section_count == 1

    assert stream.sections[0].data == data