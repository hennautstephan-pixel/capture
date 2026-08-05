from capture_recovery.validation import (
    CaptureStreamValidator,
)



def test_capture_stream_validator_empty_data():

    validator = CaptureStreamValidator()


    result = validator.validate(
        b"",
    )


    assert result.valid is False


    assert (
        "empty data"
        in result.issues
    )



def test_capture_stream_validator_returns_result():

    validator = CaptureStreamValidator()


    result = validator.validate(
        b"CAPTURE_TEST_DATA",
    )


    assert isinstance(
        result.valid,
        bool,
    )


    assert isinstance(
        result.issues,
        tuple,
    )



def test_capture_stream_validator_file(tmp_path):

    file = tmp_path / "project.c2p"


    file.write_bytes(
        b"CAPTURE_TEST_DATA"
    )


    validator = CaptureStreamValidator()


    result = validator.validate_file(
        file,
    )


    assert isinstance(
        result.streams_found,
        int,
    )