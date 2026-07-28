import json


from capture_recovery.io import (
    CaptureReader,
)


def test_capture_reader_json(
    tmp_path,
):

    file = tmp_path / "project.json"


    file.write_text(
        json.dumps(
            {
                "name": "Test Project"
            }
        ),
        encoding="utf-8",
    )


    result = (
        CaptureReader()
        .read(
            file,
        )
    )


    assert result["name"] == (
        "Test Project"
    )



def test_capture_reader_bytes(
    tmp_path,
):

    file = tmp_path / "capture.bin"


    file.write_bytes(
        b"CAPTURE",
    )


    result = (
        CaptureReader()
        .read_bytes(
            file,
        )
    )


    assert result == (
        b"CAPTURE"
    )