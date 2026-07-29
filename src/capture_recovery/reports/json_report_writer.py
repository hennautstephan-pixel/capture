"""
JSON report writer.

Exports AnalysisReport instances
to JSON files.
"""

from __future__ import annotations

import json

from pathlib import Path
from datetime import datetime, timezone

from .analysis_report import AnalysisReport



class JsonReportWriter:
    """
    Write analysis reports as JSON.
    """



    def write(
        self,
        report: AnalysisReport,
        filename: str | Path,
    ) -> Path:
        """
        Export an AnalysisReport to JSON.
        """

        if not isinstance(
            report,
            AnalysisReport,
        ):

            raise TypeError(
                "report must be an AnalysisReport"
            )



        path = Path(
            filename
        )


        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )



        data = report.to_dict()



        #
        # Metadata du rapport
        #

        data["_report"] = {

            "format":
                "capture-recovery-analysis",

            "version":
                "1.0",

            "generated":
                datetime.now(
                    timezone.utc
                ).isoformat(),

        }



        path.write_text(

            json.dumps(

                data,

                indent=4,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )


        return path