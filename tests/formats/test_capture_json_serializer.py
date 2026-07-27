from capture_recovery.formats.capture_json_serializer import (
    CaptureJsonSerializer,
)
from capture_recovery.formats.capture_project import (
    CaptureProject,
    CaptureFixture,
    CaptureUniverse,
    CaptureCue,
)


def create_capture_project():

    project = CaptureProject(
        name="Recovered Capture",
    )

    project.add_fixture(
        CaptureFixture(
            name="Mac Aura",
            universe=1,
            address=10,
            manufacturer="Martin",
            model="MAC Aura",
            mode="Standard",
        )
    )

    project.add_universe(
        CaptureUniverse(
            name="Universe 1",
            universe=1,
            protocol="sACN",
        )
    )

    project.add_cue(
        CaptureCue(
            name="Intro",
            number=1,
        )
    )

    return project


def test_to_dict():

    serializer = CaptureJsonSerializer()

    result = serializer.to_dict(
        create_capture_project(),
    )

    assert result["project"]["name"] == "Recovered Capture"

    assert len(result["fixtures"]) == 1

    assert len(result["universes"]) == 1

    assert len(result["cues"]) == 1


def test_fixture_json_data():

    serializer = CaptureJsonSerializer()

    result = serializer.to_dict(
        create_capture_project(),
    )

    fixture = result["fixtures"][0]

    assert fixture["name"] == "Mac Aura"

    assert fixture["universe"] == 1

    assert fixture["address"] == 10

    assert fixture["manufacturer"] == "Martin"


def test_universe_json_data():

    serializer = CaptureJsonSerializer()

    result = serializer.to_dict(
        create_capture_project(),
    )

    universe = result["universes"][0]

    assert universe["name"] == "Universe 1"

    assert universe["protocol"] == "sACN"


def test_cue_json_data():

    serializer = CaptureJsonSerializer()

    result = serializer.to_dict(
        create_capture_project(),
    )

    cue = result["cues"][0]

    assert cue["name"] == "Intro"

    assert cue["number"] == 1


def test_to_string():

    serializer = CaptureJsonSerializer()

    result = serializer.to_string(
        create_capture_project(),
    )

    assert isinstance(
        result,
        str,
    )

    assert "Recovered Capture" in result

    assert "Mac Aura" in result


def test_save_file(tmp_path):

    serializer = CaptureJsonSerializer()

    target = tmp_path / "capture_project.json"

    serializer.save(
        create_capture_project(),
        target,
    )

    assert target.exists()

    content = target.read_text(
        encoding="utf-8",
    )

    assert "Recovered Capture" in content