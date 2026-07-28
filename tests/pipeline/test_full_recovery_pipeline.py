from capture_recovery.pipeline import (
    FullRecoveryPipeline,
)


class FakeSemanticPipeline:

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
        )
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