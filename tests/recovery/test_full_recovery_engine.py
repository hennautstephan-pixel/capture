from pathlib import Path

from capture_recovery.recovery import (
    FullRecoveryEngine,
    RecoveryReport,
)


def test_full_recovery_engine_creation():

    engine = FullRecoveryEngine()

    assert engine is not None



def test_recovery_report_structure(tmp_path):

    report = RecoveryReport(
        source=tmp_path / "source.c2p",
        output=tmp_path / "output.c2p",
        executed_actions=0,
        skipped_actions=0,
        binary_result=None,
    )


    assert isinstance(
        report.source,
        Path,
    )

    assert report.executed_actions == 0