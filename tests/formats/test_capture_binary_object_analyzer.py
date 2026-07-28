from capture_recovery.formats import (
    CaptureBinaryObjectAnalyzer,
)


def test_capture_binary_object_analyzer(
    tmp_path,
):

    file = tmp_path / "test.c2p"


    file.write_bytes(

        b"\x20\x00\x00\x00"
        +
        b"A" * 28

    )


    analyzer = (
        CaptureBinaryObjectAnalyzer()
    )


    result = analyzer.analyze(
        file
    )


    assert result["size"] > 0

    assert "objects" in result

    assert result["count"] >= 1