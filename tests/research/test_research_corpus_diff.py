from __future__ import annotations

import zlib

from capture_recovery.research import (
    CorpusDiff,
)


def test_compare_same_file(tmp_path):

    payload = b"Hello Capture"

    compressed = zlib.compress(payload)

    data = (
        b"HEADER"
        + compressed
    )

    file = tmp_path / "sample.c2p"

    file.write_bytes(data)

    diff = CorpusDiff()

    result = diff.compare(
        file,
        file,
    )

    assert result.compressed_equal
    assert result.decompressed_equal
    assert result.changed_regions == []