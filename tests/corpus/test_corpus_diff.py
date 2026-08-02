from pathlib import Path

from capture_recovery.corpus import (
    CorpusDiff,
    CorpusDiffer,
    CorpusEntry,
)


def entry(
    *,
    size=100,
    sha="abc",
):

    return CorpusEntry(
        path=Path("sample.c2p"),
        format="capture_binary",
        size=size,
        sha256=sha,
        compressed_size=50,
        decompressed_size=120,
        stream_offset=62,
    )


def test_identical():

    diff = CorpusDiffer().compare(
        entry(),
        entry(),
    )

    assert isinstance(
        diff,
        CorpusDiff,
    )

    assert diff.identical

    assert diff.difference_count == 0


def test_size():

    diff = CorpusDiffer().compare(
        entry(size=100),
        entry(size=120),
    )

    assert diff.difference_count == 1

    assert diff.differences[0].field == "size"


def test_hash():

    diff = CorpusDiffer().compare(
        entry(sha="aaa"),
        entry(sha="bbb"),
    )

    assert diff.difference_count == 1

    assert diff.differences[0].field == "sha256"