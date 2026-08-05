from capture_recovery.pipeline import (
    FullRecoveryPipeline,
)


class FakeSemanticPipeline:
    """
    Fake semantic pipeline.
    """

    def run(
        self,
        analysis,
    ):

        return {
            "objects": [
                {
                    "type": "fixture",
                    "name": "Fixture A",
                }
            ]
        }



class FakeProject:

    pass



class FakeProjectPipeline:
    """
    Fake project recovery pipeline.

    Verifies that FullRecoveryPipeline
    delegates project creation correctly.
    """

    def recover(
        self,
        objects,
    ):

        return {
            "project": FakeProject(),

            "validation": {
                "valid": True,
                "errors": [],
            },
        }



def test_full_recovery_pipeline(
    tmp_path,
):

    file = tmp_path / "project.cap"


    file.write_bytes(
        b"CAPTURE"
        + b"\x01\x02",
    )


    pipeline = FullRecoveryPipeline(
        semantic_pipeline=(
            FakeSemanticPipeline()
        ),

        project_pipeline=(
            FakeProjectPipeline()
        ),
    )


    result = pipeline.recover(
        file,
    )


    assert result["binary"]["data"] == (
        b"CAPTURE\x01\x02"
    )


    assert len(
        result["semantic"]["objects"]
    ) == 1


    assert result["semantic"]["objects"][0]["type"] == (
        "fixture"
    )


    assert result["project"] is not None


    assert result["result"].project.valid is True
