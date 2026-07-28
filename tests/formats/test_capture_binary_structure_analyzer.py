from capture_recovery.formats import (
    CaptureBinaryStructureAnalyzer,
)


def test_capture_binary_structure_analyzer(
    tmp_path,
):

    file = tmp_path / "project.c2p"


    file.write_bytes(
        (
            b"Project"
            b"\x00"
            b"Fixture"
            b"\x00"
            b"Universe 1"
        )
    )


    analyzer = CaptureBinaryStructureAnalyzer()


    result = analyzer.analyze(
        file
    )


    assert result["size"] > 0

    assert "sha256" in result

    assert len(
        result["ascii_strings"]
    ) > 0

    assert len(
        result["blocks"]
    ) > 0