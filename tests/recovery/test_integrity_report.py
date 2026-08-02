from capture_recovery.recovery import (
    IntegrityIssue,
    IntegrityReport,
    IntegritySeverity,
)


def test_empty_report():

    report = IntegrityReport()

    assert report.count == 0
    assert report.recoverable is True
    assert report.has_issues is False


def test_add_issue():

    report = IntegrityReport()

    report.add(
        IntegrityIssue(
            code="ZIP001",
            message="Missing central directory",
            severity=IntegritySeverity.ERROR,
        )
    )

    assert report.count == 1
    assert report.error_count == 1
    assert report.has_errors is True


def test_statistics():

    report = IntegrityReport()

    report.extend(
        [
            IntegrityIssue(
                "I",
                "",
                IntegritySeverity.INFO,
            ),
            IntegrityIssue(
                "W",
                "",
                IntegritySeverity.WARNING,
            ),
            IntegrityIssue(
                "E",
                "",
                IntegritySeverity.ERROR,
            ),
            IntegrityIssue(
                "C",
                "",
                IntegritySeverity.CRITICAL,
            ),
        ]
    )

    assert report.info_count == 1
    assert report.warning_count == 1
    assert report.error_count == 1
    assert report.critical_count == 1


def test_recoverable():

    report = IntegrityReport()

    report.add(
        IntegrityIssue(
            code="ZIP001",
            message="Corrupted archive",
            severity=IntegritySeverity.CRITICAL,
            recoverable=False,
        )
    )

    assert report.recoverable is False


def test_summary():

    report = IntegrityReport()

    report.add(
        IntegrityIssue(
            code="A",
            message="",
            severity=IntegritySeverity.WARNING,
        )
    )

    assert "1 issues" in report.summary()


def test_to_dict():

    report = IntegrityReport()

    report.add(
        IntegrityIssue(
            code="A",
            message="",
            severity=IntegritySeverity.INFO,
        )
    )

    data = report.to_dict()

    assert data["count"] == 1
    assert data["recoverable"] is True