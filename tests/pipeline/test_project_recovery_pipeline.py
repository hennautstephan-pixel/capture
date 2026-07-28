from capture_recovery.pipeline import (
    ProjectRecoveryPipeline,
)


class FakeProject:

    pass



class FakeReconstructor:

    def reconstruct(
        self,
        objects,
    ):

        return FakeProject()



class FakeValidator:

    def validate(
        self,
        project,
    ):

        return []



def test_project_recovery_pipeline():

    pipeline = ProjectRecoveryPipeline(

        reconstructor=(
            FakeReconstructor()
        ),

        validator=(
            FakeValidator()
        ),

    )


    result = pipeline.recover(
        [
            {
                "type": "fixture"
            }
        ]
    )


    assert result["project"] is not None

    assert result["validation"]["valid"] is True

    assert result["validation"]["errors"] == []