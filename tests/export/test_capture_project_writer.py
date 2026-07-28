from capture_recovery.export import (
    CaptureProjectWriter,
)

from capture_recovery.formats import (
    CaptureProject,
    CaptureFixture,
)


def test_project_writer_dict():

    project = CaptureProject(
        name="Test",
    )


    project.add_fixture(
        CaptureFixture(
            name="MAC Aura",
            universe=1,
            address=20,
        )
    )


    result = (
        CaptureProjectWriter()
        .to_dict(
            project,
        )
    )


    assert result["name"] == (
        "Test"
    )


    assert len(
        result["fixtures"]
    ) == 1


    assert (
        result["fixtures"][0]["name"]
        ==
        "MAC Aura"
    )