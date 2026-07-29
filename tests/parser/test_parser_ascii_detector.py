from capture_recovery.parser.ascii_detector import AsciiDetector


def test_empty():
    assert AsciiDetector.detect(b"") == []


def test_single_string():
    data = b"\x00Hello World\x00"

    segments = AsciiDetector.detect(data)

    assert len(segments) == 1

    s = segments[0]

    assert s.offset == 1
    assert s.length == 11
    assert s.kind == "ascii"
    assert s.metadata["text"] == "Hello World"


def test_multiple_strings():
    data = b"\x00Hello\x00World\x00"

    segments = AsciiDetector.detect(data)

    assert len(segments) == 2

    assert segments[0].metadata["text"] == "Hello"
    assert segments[1].metadata["text"] == "World"


def test_ignore_short_strings():
    data = b"\x00abc\x00"

    assert AsciiDetector.detect(data) == []


def test_detect_at_end():
    data = b"\x00Capture"

    segments = AsciiDetector.detect(data)

    assert len(segments) == 1
    assert segments[0].metadata["text"] == "Capture"


def test_detect_beginning():
    data = b"Capture\x00"

    segments = AsciiDetector.detect(data)

    assert len(segments) == 1
    assert segments[0].offset == 0


def test_only_binary():
    assert AsciiDetector.detect(bytes(range(32))) == []


def test_spaces_allowed():
    data = b"\x00Lighting Project\x00"

    segments = AsciiDetector.detect(data)

    assert segments[0].metadata["text"] == "Lighting Project"