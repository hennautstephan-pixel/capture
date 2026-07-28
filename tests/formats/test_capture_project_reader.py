from capture_recovery.formats import (
    CaptureProjectReader,
)


def test_capture_project_reader_binary(
    tmp_path,
):

    project_file = (
        tmp_path
        / "test.c2p"
    )


    project_file.write_bytes(
        b"CAPTURE PROJECT"
    )


    reader = CaptureProjectReader()


    result = reader.read(
        project_file,
    )


    assert result["name"] == "test"

    assert "metadata" in result

    assert result["metadata"]["size"] > 0