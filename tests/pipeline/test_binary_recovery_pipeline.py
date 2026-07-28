from capture_recovery.pipeline import (
    BinaryRecoveryPipeline,
)


def test_binary_recovery_pipeline(
    tmp_path,
):

    file = tmp_path / "project.cap"


    file.write_bytes(
        b"CAPTURE"
        + b"\x01\x02\x03",
    )


    result = (
        BinaryRecoveryPipeline()
        .run(
            file,
        )
    )


    assert result["data"] == (
        b"CAPTURE"
        + b"\x01\x02\x03"
    )


    assert result["analysis"]["size"] == (
        10
    )


    assert (
        result["analysis"]["signature"]
        ==
        b"CAPTURE\x01\x02\x03"
    )