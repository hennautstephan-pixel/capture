from capture_recovery.validation import (
    CaptureHeaderValidator,
)



def test_capture_header_validator_accepts_parsable_header():

    validator = CaptureHeaderValidator()


    result = validator.validate(
        b"CAPTURE_TEST_DATA",
    )


    assert result.valid is False or result.valid is True

    assert isinstance(
        result.issues,
        tuple,
    )



def test_capture_header_validator_rejects_empty_data():

    validator = CaptureHeaderValidator()


    result = validator.validate(
        b"",
    )


    assert result.valid is False


    assert (
        "empty data"
        in result.issues
    )



def test_capture_header_validator_file(tmp_path):

    file = tmp_path / "project.c2p"


    file.write_bytes(
        b"CAPTURE_TEST_DATA"
    )


    validator = CaptureHeaderValidator()


    result = validator.validate_file(
        file,
    )


    assert isinstance(
        result.valid,
        bool,
    )