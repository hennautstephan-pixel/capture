from capture_recovery.reconstruction import ReconstructionContext


def test_size():
    ctx = ReconstructionContext(
        data=b"abcdef",
    )

    assert ctx.size == 6


def test_slice():
    ctx = ReconstructionContext(
        data=b"abcdef",
    )

    assert ctx.slice(1, 3) == b"bcd"


def test_contains():
    ctx = ReconstructionContext(
        data=b"abcdef",
    )

    assert ctx.contains(b"cd")
    assert not ctx.contains(b"zz")


def test_metadata():
    ctx = ReconstructionContext(
        data=b"",
        metadata={"version": 17},
    )

    assert ctx.has_metadata("version")
    assert ctx.metadata_value("version") == 17


def test_describe():
    ctx = ReconstructionContext(
        data=b"1234",
    )

    d = ctx.describe()

    assert d["size"] == 4