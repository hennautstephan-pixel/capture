from capture_recovery.recovery import (
    IntegrityIssue,
    IntegritySeverity,
)


def test_issue_creation():

    issue = IntegrityIssue(
        code="ZIP001",
        message="Missing central directory",
        severity=IntegritySeverity.CRITICAL,
    )

    assert issue.code == "ZIP001"
    assert issue.severity is IntegritySeverity.CRITICAL
    assert issue.recoverable is True


def test_fatal_issue():

    issue = IntegrityIssue(
        code="ZIP001",
        message="Corrupted archive",
        severity=IntegritySeverity.CRITICAL,
        recoverable=False,
    )

    assert issue.fatal is True


def test_non_fatal_issue():

    issue = IntegrityIssue(
        code="JSON001",
        message="Missing optional field",
        severity=IntegritySeverity.WARNING,
    )

    assert issue.fatal is False


def test_string_without_location():

    issue = IntegrityIssue(
        code="GUID001",
        message="Duplicate GUID",
        severity=IntegritySeverity.ERROR,
    )

    assert (
        str(issue)
        == "[ERROR] Duplicate GUID"
    )


def test_string_with_location():

    issue = IntegrityIssue(
        code="GUID001",
        message="Duplicate GUID",
        severity=IntegritySeverity.ERROR,
        location="/Scene/Fixture1",
    )

    assert (
        str(issue)
        == "[ERROR] /Scene/Fixture1: Duplicate GUID"
    )