from capture_recovery.reports import (
    AnalysisReport,
)


def test_analysis_report_creation():

    result = {

        "binary": {

            "analysis": {

                "size": 100,

                "detections": [],

                "count": 3,

                "reverse": None,

            }

        },

        "semantic": {

            "objects": [

                {

                    "type": "fixture"

                }

            ]

        }

    }


    report = AnalysisReport.from_pipeline_result(
        "test.c2p",
        result,
    )


    assert report.filesize == 100

    assert report.semantic.objects == 1

    assert report.binary.blocks == 3