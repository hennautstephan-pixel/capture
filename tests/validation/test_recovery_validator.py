from capture_recovery.validation import (
    RecoveryValidator,
)



def test_validator_accepts_identical_data():

    validator = RecoveryValidator()


    result = validator.validate(
        b"CAPTURE_DATA",
        b"CAPTURE_DATA",
    )


    assert result.valid is True

    assert result.score == 1.0



def test_validator_detects_difference():

    validator = RecoveryValidator()


    result = validator.validate(
        b"AAAA",
        b"BBBB",
    )


    assert result.valid is False

    assert (
        "Low binary similarity"
        in result.issues
    )