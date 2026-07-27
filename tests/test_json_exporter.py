import json

from src.capture_recovery.exporters import JsonExporter
from src.capture_recovery.models import (
    Block,
    Detection,
    Report,
)


def test_json_exporter(tmp_path):

    report = Report(
        filename="test.c2p",
        filesize=1024,
    )

    report.detections.append(
        Detection(
            datatype="ascii",
            offset=10,
            length=5,
            value="Hello",
            confidence=1.0,
        )
    )

    report.blocks.append(
        Block(
            name="Header",
            offset=0,
            length=64,
        )
    )

    exporter = JsonExporter()

    filename = tmp_path / "report.json"

    exporter.export(report, filename)

    data = json.loads(filename.read_text())

    assert "detections" in data
    assert "blocks" in data

    assert len(data["detections"]) == 1
    assert len(data["blocks"]) == 1

    assert data["detections"][0]["datatype"] == "ascii"
    assert data["blocks"][0]["name"] == "Header"