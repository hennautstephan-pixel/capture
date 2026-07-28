from capture_recovery.pipeline import (
    CaptureProjectPipeline,
)


def test_capture_project_pipeline(
    tmp_path,
):

    project_file = (
        tmp_path
        / "project.c2p"
    )


    project_file.write_bytes(
        b"CAPTURE PROJECT DATA"
    )


    pipeline = CaptureProjectPipeline()


    result = pipeline.process(
        project_file,
    )


    assert result["success"] is True

    assert result["source"] == str(
        project_file
    )

    assert "project" in result

    assert "metadata" in result