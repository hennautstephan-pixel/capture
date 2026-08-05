from pathlib import Path

from capture_recovery.recovery import (
    RecoveryReportGenerator,
    RecoveryReport,
    FullRecoveryResult,
)

from capture_recovery.reconstruction import (
    ReconstructionPlan,
)



def test_generate_report(tmp_path):

    result = FullRecoveryResult(
        source=tmp_path / "source.c2p",
        output=tmp_path / "output.c2p",
        plans=(
            ReconstructionPlan(
                object_type="fixture",
                offset=10,
                size=4,
                replacement=b"DATA",
                source="sample.c2p",
                confidence=0.9,
            ),
        ),
        restored_objects=1,
    )


    generator = RecoveryReportGenerator()


    report = generator.generate(
        result,
    )


    assert isinstance(
        report,
        RecoveryReport,
    )


    assert (
        report.objects_restored
        ==
        1
    )


    assert (
        report.confidence
        ==
        0.9
    )



def test_save_report_json(tmp_path):

    report = RecoveryReport(
        source="source.c2p",
        output="output.c2p",
        objects_restored=2,
        plans=2,
        confidence=0.95,
        status="success",
    )


    destination = (
        tmp_path /
        "report.json"
    )


    RecoveryReportGenerator().save_json(
        report,
        destination,
    )


    assert destination.exists()

    assert (
        "objects_restored"
        in destination.read_text(
            encoding="utf-8"
        )
    )