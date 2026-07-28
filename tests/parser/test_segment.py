from capture_recovery.parser.segment import Segment


def test_end():
    s = Segment(10, 5)

    assert s.end == 15


def test_contains():
    s = Segment(100, 20)

    assert s.contains(100)
    assert s.contains(110)

    assert not s.contains(120)
    assert not s.contains(99)


def test_overlap():
    a = Segment(0, 10)
    b = Segment(5, 10)
    c = Segment(20, 5)

    assert a.overlaps(b)

    assert not a.overlaps(c)


def test_children():
    parent = Segment(0, 100)

    child = Segment(10, 20)

    parent.add_child(child)

    assert len(parent.children) == 1

    assert parent.children[0] is child


def test_len():
    s = Segment(0, 42)

    assert len(s) == 42