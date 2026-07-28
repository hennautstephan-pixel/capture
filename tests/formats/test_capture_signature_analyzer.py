from capture_recovery.formats import (
    CaptureSignatureAnalyzer,
)



def test_capture_signature_analyzer(
    tmp_path,
):


    file = tmp_path / "test.c2p"


    file.write_bytes(

        b"ABCDEFGH"

        +

        b"12345678"

        +

        b"ABCDEFGH"

    )


    analyzer = (
        CaptureSignatureAnalyzer()
    )


    result = analyzer.analyze(
        file
    )


    assert result["size"] > 0


    assert (
        "signatures"
        in result
    )


    assert (
        result["signature_count"]
        >=
        1
    )