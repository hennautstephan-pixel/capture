from capture_recovery.pipeline import (
    SemanticRecoveryPipeline,
)


class FakeBuilder:

    def build(
        self,
        detections,
    ):

        return [

            {

                "type": "fixture",

                "name": "Test Fixture",

            }

        ]



def test_semantic_recovery_pipeline():

    pipeline = SemanticRecoveryPipeline(
        builders=[
            FakeBuilder()
        ]
    )


    result = pipeline.run(
        {

            "detections": [

                "fixture"

            ]

        }
    )


    assert len(
        result["objects"]
    ) == 1


    assert result["objects"][0]["type"] == (
        "fixture"
    )