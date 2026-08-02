from capture_recovery.parser import (
    CaptureHeader,
    HeaderParser,
)


def test_parser_creation():

    parser = HeaderParser()

    assert isinstance(
        parser,
        HeaderParser,
    )


def test_empty_header():

    header = HeaderParser().parse(
        b"",
    )

    assert isinstance(
        header,
        CaptureHeader,
    )

    assert header.size == 0

    assert not header.is_valid


def test_header_size():

    data = bytes(range(32))

    header = HeaderParser().parse(
        data,
    )

    assert header.size == 32


def test_magic():

    data = bytes(range(32))

    header = HeaderParser().parse(
        data,
    )

    assert header.magic == data[:8]


def test_raw_preserved():

    data = bytes(range(64))

    header = HeaderParser().parse(
        data,
    )

    assert header.raw == data[:32]