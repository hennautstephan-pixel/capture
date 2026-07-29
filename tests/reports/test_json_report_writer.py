from pathlib import Path

import json


from capture_recovery.reports import (
    AnalysisReport,
    JsonReportWriter,
)



def test_json_report_writer(
    tmp_path,
):

    report = AnalysisReport(
        filename="broken.c2p",
        filesize=1024,
    )


    output = tmp_path / "report.json"


    writer = JsonReportWriter()


    result = writer.write(
        report,
        output,
    )


    assert result == output

    assert output.exists()


    data = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )


    assert data["filename"] == (
        "broken.c2p"
    )


    assert data["filesize"] == 1024