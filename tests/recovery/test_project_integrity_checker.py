from capture_recovery.recovery import (
    IntegrityReport,
    ProjectIntegrityChecker,
)


class DummyCheck:

    def check(
        self,
        project,
        report: IntegrityReport,
    ) -> None:

        project["called"] = True


def test_empty_checker():

    checker = ProjectIntegrityChecker()

    report = checker.check({})

    assert isinstance(
        report,
        IntegrityReport,
    )


def test_calls_checks():

    checker = ProjectIntegrityChecker()

    checker.add_check(
        DummyCheck(),
    )

    project = {}

    checker.check(project)

    assert project["called"] is True