import zlib

from capture_recovery.parser import (
    DecompressedStream,
    StreamDecompressor,
)


def test_empty():

    result = StreamDecompressor().decompress(
        b"",
        offset=0,
    )

    assert result.is_empty


def test_decompress():

    payload = b"hello capture"

    compressed = zlib.compress(
        payload,
    )

    result = StreamDecompressor().decompress(
        compressed,
        offset=0,
    )

    assert result.decompressed == payload

    assert result.compressed_size == len(compressed)


def test_can_decompress():

    payload = zlib.compress(
        b"abcd",
    )

    assert StreamDecompressor().can_decompress(
        payload,
        offset=0,
    )


def test_invalid():

    assert not StreamDecompressor().can_decompress(
        b"abcdef",
        offset=0,
    )