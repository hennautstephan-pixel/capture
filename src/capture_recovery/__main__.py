"""
Capture Recovery CLI entry point.
"""

from __future__ import annotations


import argparse


from capture_recovery.pipeline import (
    FullRecoveryPipeline,
)


from capture_recovery.reports.analysis_report import (
    AnalysisReport,
)


from capture_recovery.reports.json_report_writer import (
    JsonReportWriter,
)



def analyze_command(
    filename: str,
    report_file: str,
) -> None:
    """
    Execute Capture recovery analysis.
    """


    pipeline = FullRecoveryPipeline()



    result = pipeline.recover(
        filename,
    )



    report = AnalysisReport.from_pipeline_result(
        filename,
        result,
    )



    writer = JsonReportWriter()



    writer.write(
        report,
        report_file,
    )



    print(
        report.summary()
    )



    print(
        f"\nReport written: {report_file}"
    )



def main():

    parser = argparse.ArgumentParser(

        prog="capture_recovery",

        description=(

            "Capture project recovery tool"

        ),

    )



    commands = parser.add_subparsers(

        dest="command",

        required=True,

    )



    analyze = commands.add_parser(

        "analyze",

        help="Analyze Capture file",

    )



    analyze.add_argument(

        "file",

        help="Input .c2p file",

    )



    analyze.add_argument(

        "--report",

        required=True,

        help="JSON output report",

    )



    args = parser.parse_args()



    if args.command == "analyze":


        analyze_command(

            args.file,

            args.report,

        )



if __name__ == "__main__":

    main()