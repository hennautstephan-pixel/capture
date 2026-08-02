from pathlib import Path

from capture_recovery.research import (
    CorpusAnalysis,
    CorpusStream,
)


def test_stream():

    stream = CorpusStream(
        offset=62,
        compressed_size=1189,
        decompressed_size=11676,
        trailing_bytes=8,
        footer=b"12345678",
        decompressed=b"",
    )

    assert stream.offset == 62
    assert stream.trailing_bytes == 8
    assert len(stream.footer) == 8


def test_analysis():

    analysis = CorpusAnalysis(
        path=Path("sample.c2p"),
        file_size=1259,
        stream=CorpusStream(
            offset=62,
            compressed_size=1189,
            decompressed_size=11676,
            trailing_bytes=8,
            footer=b"12345678",
            decompressed=b"",
        ),
        header_size=62,
    )

    assert analysis.file_size == 1259
    assert analysis.header_size == 62