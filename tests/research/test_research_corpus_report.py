from __future__ import annotations

import zlib

from capture_recovery.research import (
    CorpusReport,
    CorpusReportGenerator,
)


def create_project(
    path,
    payload: bytes,
):

    path.write_bytes(
        b"HEADER"
        + zlib.compress(payload)
    )


def test_generate_empty_directory(tmp_path):

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    assert isinstance(
        report,
        CorpusReport,
    )

    assert report.project_count == 0

    assert report.total_file_size == 0

    assert report.total_compressed_size == 0

    assert report.total_decompressed_size == 0

    assert report.average_compression_ratio == 0

    assert report.projects == []

    assert "# Capture Corpus Report" in report.markdown

    assert "No Capture projects found." in report.markdown


def test_generate_single_project(tmp_path):

    create_project(
        tmp_path / "sample.c2p",
        b"Hello Capture",
    )

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    assert report.project_count == 1

    assert report.total_file_size > 0

    assert report.total_compressed_size > 0

    assert report.total_decompressed_size == len(
        b"Hello Capture"
    )

    assert report.average_compression_ratio > 0

    assert len(report.projects) == 1

    assert (
        report.projects[0].path.name
        == "sample.c2p"
    )


def test_generate_multiple_projects(tmp_path):

    create_project(
        tmp_path / "one.c2p",
        b"AAAAAA",
    )

    create_project(
        tmp_path / "two.c2p",
        bytes(range(128)),
    )

    create_project(
        tmp_path / "three.c2p",
        bytes(range(64)) * 4,
    )

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    assert report.project_count == 3

    assert len(report.projects) == 3

    assert report.total_file_size > 0

    assert report.total_compressed_size > 0

    assert report.total_decompressed_size > 0


def test_markdown_contains_table(tmp_path):

    create_project(
        tmp_path / "sample.c2p",
        b"Hello Capture",
    )

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    markdown = report.markdown

    assert "# Capture Corpus Report" in markdown

    assert "## Summary" in markdown

    assert "## Projects" in markdown

    assert "| Project |" in markdown

    assert "sample.c2p" in markdown


def test_write_report(tmp_path):

    create_project(
        tmp_path / "sample.c2p",
        b"Hello Capture",
    )

    destination = (
        tmp_path
        / "report.md"
    )

    generator = CorpusReportGenerator()

    report = generator.write(
        tmp_path,
        destination,
    )

    assert destination.exists()

    assert (
        destination.read_text(
            encoding="utf-8",
        )
        == report.markdown
    )


def test_report_totals(tmp_path):

    create_project(
        tmp_path / "a.c2p",
        b"Hello",
    )

    create_project(
        tmp_path / "b.c2p",
        bytes(range(256)),
    )

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    assert (
        report.total_file_size
        == sum(
            p.file_size
            for p in report.projects
        )
    )

    assert (
        report.total_compressed_size
        == sum(
            p.compressed_size
            for p in report.projects
        )
    )

    assert (
        report.total_decompressed_size
        == sum(
            p.decompressed_size
            for p in report.projects
        )
    )


def test_report_project_order(tmp_path):

    create_project(
        tmp_path / "zeta.c2p",
        b"1",
    )

    create_project(
        tmp_path / "alpha.c2p",
        b"2",
    )

    generator = CorpusReportGenerator()

    report = generator.generate(
        tmp_path,
    )

    names = [
        project.path.name
        for project in report.projects
    ]

    assert names == sorted(names)