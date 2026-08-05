from capture_recovery.validation import (
    ReconstructionValidator,
    ValidationResult,
)


class FakeProjectValidator:
    """
    Fake validator used to verify delegation.
    """

    def __init__(self):
        self.called = False
        self.received = None

    def validate(
        self,
        project,
    ):
        self.called = True
        self.received = project

        return ValidationResult()



def test_reconstruction_validator_delegates_to_project_validator():

    fake_validator = FakeProjectValidator()

    validator = ReconstructionValidator(
        project_validator=fake_validator,
    )

    project = object()

    result = validator.validate(
        project,
    )

    assert isinstance(
        result,
        ValidationResult,
    )

    assert fake_validator.called is True

    assert (
        fake_validator.received
        is project
    )



def test_reconstruction_validator_returns_project_validation_result():

    validator = ReconstructionValidator()

    project = object()

    result = validator.validate(
        project,
    )

    assert isinstance(
        result,
        ValidationResult,
    )