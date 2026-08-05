from __future__ import annotations

import json

from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass(slots=True, frozen=True)
class RecoveryReport:
    """
    Unified recovery report.

    Compatible with:
    - FullRecoveryEngine
    - FullRecoveryPipeline
    - RecoveryReportGenerator
    """

    source: Path | str

    output: Path | str

    executed_actions: int = 0

    skipped_actions: int = 0

    binary_result: object | None = None

    objects_restored: int = 0

    plans: int = 0

    confidence: float = 0.0

    status: str = "unknown"



class RecoveryReportGenerator:
    """
    Generate serializable recovery reports.
    """


    def generate(
        self,
        result,
    ) -> RecoveryReport:
        """
        Convert recovery result into report.
        """

        plans = getattr(
            result,
            "plans",
            (),
        )


        restored = getattr(
            result,
            "restored_objects",
            0,
        )


        confidence = 0.0


        if plans:

            confidence = (
                sum(
                    plan.confidence
                    for plan in plans
                )
                /
                len(plans)
            )


        return RecoveryReport(
            source=result.source,
            output=result.output,
            executed_actions=restored,
            skipped_actions=0,
            binary_result=None,
            objects_restored=restored,
            plans=len(plans),
            confidence=confidence,
            status=(
                "success"
                if restored
                else "no_changes"
            ),
        )



    def save_json(
        self,
        report: RecoveryReport,
        destination: Path,
    ) -> None:
        """
        Save report as JSON.
        """

        data = asdict(
            report,
        )


        data["source"] = str(
            data["source"]
        )

        data["output"] = str(
            data["output"]
        )


        destination.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )



    def to_dict(
        self,
        report: RecoveryReport,
    ) -> dict:
        """
        Convert report to dictionary.
        """

        data = asdict(
            report,
        )

        data["source"] = str(
            data["source"]
        )

        data["output"] = str(
            data["output"]
        )

        return data