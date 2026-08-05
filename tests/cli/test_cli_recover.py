from pathlib import Path

from capture_recovery.cli.recover import (
    build_parser,
    recover_file,
)



def test_recover_cli_parser(tmp_path):

    parser = build_parser()


    args = parser.parse_args(
        [
            str(tmp_path / "source.c2p"),
            "--reference",
            str(tmp_path / "reference.c2p"),
            "--corpus",
            str(tmp_path),
            "--output",
            str(tmp_path / "output.c2p"),
        ]
    )


    assert (
        args.source
        ==
        tmp_path / "source.c2p"
    )


    assert (
        args.reference
        ==
        tmp_path / "reference.c2p"
    )


    assert (
        args.corpus
        ==
        tmp_path
    )


    assert (
        args.output
        ==
        tmp_path / "output.c2p"
    )



def test_recover_file_with_empty_corpus(tmp_path):

    source = tmp_path / "source.c2p"

    reference = tmp_path / "reference.c2p"

    output = tmp_path / "output.c2p"

    corpus = tmp_path / "corpus"


    corpus.mkdir()


    source.write_bytes(
        b"CAPTURE_TEST_DATA"
    )

    reference.write_bytes(
        b"CAPTURE_TEST_DATA"
    )


    result = recover_file(
        source=source,
        reference=reference,
        corpus=corpus,
        output=output,
    )


    assert result == 0



def test_recover_file_generates_report(tmp_path):

    source = tmp_path / "source.c2p"

    reference = tmp_path / "reference.c2p"

    output = tmp_path / "output.c2p"

    corpus = tmp_path / "corpus"

    report = tmp_path / "report.json"


    corpus.mkdir()


    source.write_bytes(
        b"CAPTURE_TEST_DATA"
    )

    reference.write_bytes(
        b"CAPTURE_TEST_DATA"
    )


    result = recover_file(
        source=source,
        reference=reference,
        corpus=corpus,
        output=output,
        report_path=report,
    )


    assert result == 0


    assert report.exists()


    content = report.read_text(
        encoding="utf-8"
    )


    assert (
        "objects_restored"
        in content
    )