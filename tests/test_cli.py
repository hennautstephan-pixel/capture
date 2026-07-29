from __future__ import annotations

import json
import subprocess
import sys



def test_cli_analyze(tmp_path):

    c2p = tmp_path / "test.c2p"

    c2p.write_bytes(
        b"CAPTURE"
        + bytes(range(32))
    )


    report = tmp_path / "report.json"


    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "capture_recovery",
            "analyze",
            str(c2p),
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
    )


    assert result.returncode == 0, result.stderr


    assert report.exists()


    data = json.loads(
        report.read_text(
            encoding="utf-8"
        )
    )


    assert data["filename"] == str(c2p)

    assert "binary" in data

    assert "reverse" in data

    assert "semantic" in data