from pathlib import Path

from capture_recovery.cli.intelligent_analyze import (
    analyze_file,
    main,
)


def test_intelligent_analyze_file(tmp_path, capsys):
    """
    Test intelligent analysis entry point.

    Uses a minimal corpus file and verifies
    that the CLI pipeline starts correctly.
    """

    corpus_file = tmp_path / "corpus_knowledge.json"

    corpus_file.write_text(
        """
        {
            "samples": [],
            "knowledge": [
                {
                    "category": "fixture",
                    "description": "Large block added",
                    "confidence": 0.9
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    sample_file = tmp_path / "test.c2p"

    sample_file.write_bytes(
        b"CAPTURE_TEST_DATA"
    )

    result = analyze_file(
        sample_file,
        corpus_file,
    )

    assert result == 0


def test_cli_parser(monkeypatch, tmp_path):

    corpus_file = tmp_path / "corpus.json"

    corpus_file.write_text(
        """
        {
            "samples": [],
            "knowledge": []
        }
        """,
        encoding="utf-8",
    )

    sample_file = tmp_path / "test.c2p"

    sample_file.write_bytes(
        b"TEST"
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "intelligent_analyze",
            str(sample_file),
            "--corpus",
            str(corpus_file),
        ],
    )

    assert main() == 0