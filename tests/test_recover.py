from capture_recovery import (
    recover,
)



class FakeProject:

    pass



class FakeReconstructor:

    def reconstruct(
        self,
        objects,
    ):

        return FakeProject()



def test_recover(
    tmp_path,
):

    file = tmp_path / "project.cap"


    file.write_bytes(
        b"CAPTURE"
    )


    result = recover(
        file,
        reconstructor=FakeReconstructor(),
    )


    assert result["project"] is not None


    assert result["validation"]["valid"]