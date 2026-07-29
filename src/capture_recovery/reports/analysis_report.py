"""
capture_recovery.reports.analysis_report

Unified analysis report model.

Keeps compatibility with the
legacy reporting API.
"""

from __future__ import annotations


from dataclasses import (
    dataclass,
    field,
    asdict,
)



@dataclass(slots=True)
class BinarySummary:
    """
    Legacy binary report compatibility.
    """

    size: int = 0

    detections: int = 0

    blocks: int = 0



@dataclass(slots=True)
class SemanticSummary:
    """
    Legacy semantic report compatibility.
    """

    objects: int = 0



@dataclass(slots=True)
class AnalysisReport:
    """
    Complete recovery analysis report.
    """

    filename: str

    filesize: int


    #
    # New recovery model
    #

    binary_findings: list = field(
        default_factory=list
    )


    reverse_findings: int = 0


    recovered_objects: list = field(
        default_factory=list
    )


    confidence_score: int = 0


    evidence: dict = field(
        default_factory=dict
    )


    #
    # Legacy compatibility
    #

    binary: BinarySummary = field(
        default_factory=BinarySummary
    )


    semantic: SemanticSummary = field(
        default_factory=SemanticSummary
    )



    @classmethod
    def from_pipeline_result(
        cls,
        filename,
        result: dict,
    ):
        """
        Build report from pipeline result.
        """

        binary = result.get(
            "binary",
            {},
        )


        binary_analysis = binary.get(
            "analysis",
            binary,
        )



        semantic = result.get(
            "semantic",
            {},
        )



        binary_findings = (
            binary_analysis.get(
                "detections",
                [],
            )
        )



        recovered_objects = (
            semantic.get(
                "objects",
                [],
            )
        )



        evidence = (
            semantic.get(
                "evidence",
                {},
            )
        )



        reverse_findings = 0


        reverse = binary_analysis.get(
            "reverse",
        )


        if reverse is not None:

            reverse_findings = getattr(
                reverse,
                "total",
                0,
            )



        reverse_result = result.get(
            "reverse",
        )


        if (
            reverse_findings == 0
            and reverse_result is not None
        ):

            reverse_findings = getattr(
                reverse_result,
                "total",
                0,
            )



        return cls(

            filename=str(
                filename
            ),


            filesize=cls._extract_size(
                binary_analysis
            ),


            binary_findings=binary_findings,


            reverse_findings=reverse_findings,


            recovered_objects=recovered_objects,


            confidence_score=cls._calculate_confidence(

                binary_findings,

                recovered_objects,

                evidence,

            ),


            evidence=evidence,



            #
            # Legacy
            #

            binary=BinarySummary(

                size=binary_analysis.get(
                "size",
                     0,
                ),

                detections=len(
                     binary_findings
              ),

                 blocks=binary_analysis.get(
                    "count",
                     0,
                ),

            ),



            semantic=SemanticSummary(

                objects=len(
                    recovered_objects
                ),

            ),

        )



    @staticmethod
    def _extract_size(
        binary_analysis,
    ):

        return binary_analysis.get(
            "size",
            0,
        )



    @staticmethod
    def _calculate_confidence(
        binary_findings,
        recovered_objects,
        evidence,
    ):

        score = 0



        if binary_findings:

            score += 20



        if recovered_objects:

            score += 40



        if evidence.get(
            "strings",
            [],
        ):

            score += 15



        if evidence.get(
            "guids",
            [],
        ):

            score += 15



        if evidence.get(
            "numeric",
            [],
        ):

            score += 10



        return min(
            score,
            100,
        )



    def to_dict(
        self,
    ) -> dict:
        """
        Convert report to JSON.

        Keeps legacy JSON structure.
        """

        data = asdict(
            self
        )


        data["reverse"] = {

            "findings":
                self.reverse_findings,

        }


        return data



    def summary(
        self,
    ) -> str:
        """
        Human readable summary.
        """

        lines = [

            f"File: {self.filename}",

            f"Size: {self.filesize} bytes",

            "",

            (
                "Binary findings: "
                f"{len(self.binary_findings)}"
            ),

            (
                "Reverse findings: "
                f"{self.reverse_findings}"
            ),

            (
                "Recovered objects: "
                f"{len(self.recovered_objects)}"
            ),

        ]



        if self.evidence:


            lines.extend(

                [

                    "",

                    "Evidence:",


                    (
                        "  Strings: "
                        f"{len(self.evidence.get('strings', []))}"
                    ),


                    (
                        "  GUIDs: "
                        f"{len(self.evidence.get('guids', []))}"
                    ),


                    (
                        "  Numeric: "
                        f"{len(self.evidence.get('numeric', []))}"
                    ),

                ]

            )



        lines.append(

            (
                "Confidence: "
                f"{self.confidence_score}%"
            )

        )


        return "\n".join(
            lines
        )