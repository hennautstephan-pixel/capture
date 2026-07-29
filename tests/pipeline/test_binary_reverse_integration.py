from capture_recovery.pipeline import BinaryRecoveryPipeline


def test_binary_pipeline_runs_reverse(
    tmp_path,
):

    file = tmp_path / "broken.c2p"

    file.write_bytes(
        b"CAPTURE"
        + b"\x01\x02\x03"
        + b"Fixture"
    )


    pipeline = BinaryRecoveryPipeline()


    result = pipeline.run(
        file
    )


    assert "reverse" in (
        result["analysis"]
    )


    assert result["analysis"]["reverse"].total >= 0