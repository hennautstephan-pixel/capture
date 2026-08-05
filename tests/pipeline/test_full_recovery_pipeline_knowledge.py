from __future__ import annotations

from capture_recovery.pipeline import (
    FullRecoveryPipeline,
)

from capture_recovery.knowledge import (
    KnowledgeResult,
)

from capture_recovery.models import (
    Detection,
    DataType,
)


class FakeKnowledgePipeline:
    """
    Fake knowledge pipeline.

    Simulates decoded semantic objects.
    """

    def analyze(
        self,
        detections,
    ):

        result = KnowledgeResult()

        result.add_object(
            FakeSemanticObject()
        )

        return result



class FakeSemanticObject:
    """
    Minimal object compatible with
    ReconstructionRules.
    """

    object_type = "fixture"

    identifier = "Fixture_Knowledge_1"

    confidence = 1.0

    properties = {
        "manufacturer": "Test",
        "model": "Fixture",
        "universe": 1,
        "address": 1,
    }



class FakeSemanticPipeline:
    """
    Existing semantic pipeline replacement.
    """

    def run(
        self,
        analysis,
    ):

        return {
            "objects": [],
            "result": None,
        }



class FakeProject:

    pass



class FakeProjectPipeline:

    def recover(
        self,
        objects,
    ):

        assert len(objects) == 1

        assert (
            objects[0].object_type
            ==
            "fixture"
        )

        return {

            "project": FakeProject(),

            "validation": {
                "valid": True,
                "errors": [],
            },

            "result": None,
        }



class FakeBinaryPipeline:

    class Result:

        detections = []

    def run(
        self,
        path,
    ):

        return {

            "data": b"CAPTURE",

            "analysis": {

                "detections": [],

            },

            "result": self.Result(),

        }



def test_full_recovery_pipeline_with_knowledge(
    tmp_path,
):

    file = tmp_path / "project.cap"


    file.write_bytes(
        b"CAPTURE",
    )


    pipeline = FullRecoveryPipeline(

        binary_pipeline=(
            FakeBinaryPipeline()
        ),

        semantic_pipeline=(
            FakeSemanticPipeline()
        ),

        knowledge_pipeline=(
            FakeKnowledgePipeline()
        ),

        project_pipeline=(
            FakeProjectPipeline()
        ),

    )


    result = pipeline.recover(
        file,
    )


    assert result["project"] is not None


    assert (
        result["result"].project.valid
        is True
    )