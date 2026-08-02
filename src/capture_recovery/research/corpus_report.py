from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .corpus_statistics import (
    CorpusStatistics,
    CorpusStatisticsAnalyzer,
)


@dataclass(slots=True, frozen=True)
class CorpusReport:
    """
    Human-readable report generated from a Capture corpus.
    """

    directory: Path

    project_count: int

    total_file_size: int

    total_compressed_size: int

    total_decompressed_size: int

    average_compression_ratio: float

    projects: list[CorpusStatistics]

    markdown: str


class CorpusReportGenerator:
    """
    Generate Markdown reports describing a corpus of
    Capture projects.

    This class performs no reverse engineering.
    It simply aggregates objective statistics.
    """

    def __init__(
        self,
        analyzer: CorpusStatisticsAnalyzer | None = None,
    ) -> None:

        self._analyzer = analyzer or CorpusStatisticsAnalyzer()

    def generate(
        self,
        directory: str | Path,
        pattern: str = "*.c2p",
    ) -> CorpusReport:

        directory = Path(directory)

        projects = self._analyzer.analyze_directory(
            directory,
            pattern,
        )

        total_file_size = sum(
            project.file_size
            for project in projects
        )

        total_compressed = (
            self._analyzer.total_compressed_size(
                projects
            )
        )

        total_decompressed = (
            self._analyzer.total_decompressed_size(
                projects
            )
        )

        average_ratio = (
            self._analyzer.average_compression_ratio(
                projects
            )
        )

        markdown = self._build_markdown(
            directory=directory,
            projects=projects,
            total_file_size=total_file_size,
            total_compressed=total_compressed,
            total_decompressed=total_decompressed,
            average_ratio=average_ratio,
        )

        return CorpusReport(
            directory=directory,
            project_count=len(projects),
            total_file_size=total_file_size,
            total_compressed_size=total_compressed,
            total_decompressed_size=total_decompressed,
            average_compression_ratio=average_ratio,
            projects=projects,
            markdown=markdown,
        )

    def write(
        self,
        directory: str | Path,
        destination: str | Path,
        pattern: str = "*.c2p",
    ) -> CorpusReport:

        report = self.generate(
            directory,
            pattern,
        )

        destination = Path(destination)

        destination.write_text(
            report.markdown,
            encoding="utf-8",
        )

        return report

    @staticmethod
    def _build_markdown(
        *,
        directory: Path,
        projects: list[CorpusStatistics],
        total_file_size: int,
        total_compressed: int,
        total_decompressed: int,
        average_ratio: float,
    ) -> str:

        lines: list[str] = []

        lines.append("# Capture Corpus Report")
        lines.append("")

        lines.append("## Summary")
        lines.append("")
        lines.append(f"- Directory: `{directory}`")
        lines.append(f"- Projects: {len(projects)}")
        lines.append(
            f"- Total file size: {total_file_size}"
        )
        lines.append(
            f"- Total compressed size: {total_compressed}"
        )
        lines.append(
            f"- Total decompressed size: {total_decompressed}"
        )
        lines.append(
            f"- Average compression ratio: {average_ratio:.2f}"
        )

        lines.append("")
        lines.append("## Projects")
        lines.append("")

        if not projects:

            lines.append("_No Capture projects found._")

            return "\n".join(lines)

        lines.append(
            "| Project | File | Header | Compressed | Decompressed | Ratio | Footer |"
        )
        lines.append(
            "|---------|-----:|-------:|-----------:|-------------:|------:|-------:|"
        )

        for project in projects:

            lines.append(
                "| "
                f"{project.path.name} | "
                f"{project.file_size} | "
                f"{project.header_size} | "
                f"{project.compressed_size} | "
                f"{project.decompressed_size} | "
                f"{project.compression_ratio:.2f} | "
                f"{project.trailing_bytes} |"
            )

        return "\n".join(lines)