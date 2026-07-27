from capture_recovery.formats.capture_json_loader import (
    CaptureJsonLoader,
)
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
        metadata={
            "version": 1,
        },
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


def test_from_dict():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    source = create_capture_project()

    data = serializer.to_dict(
        source,
    )

    result = loader.from_dict(
        data,
    )

    assert isinstance(
        result,
        CaptureProject,
    )

    assert result.name == "Recovered Capture"


def test_load_fixture():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    result = loader.from_dict(
        serializer.to_dict(
            create_capture_project(),
        )
    )

    assert len(result.fixtures) == 1

    fixture = result.fixtures[0]

    assert fixture.name == "Mac Aura"

    assert fixture.universe == 1

    assert fixture.address == 10

    assert fixture.manufacturer == "Martin"


def test_load_universe():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    result = loader.from_dict(
        serializer.to_dict(
            create_capture_project(),
        )
    )

    assert len(result.universes) == 1

    universe = result.universes[0]

    assert universe.name == "Universe 1"

    assert universe.protocol == "sACN"


def test_load_cue():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    result = loader.from_dict(
        serializer.to_dict(
            create_capture_project(),
        )
    )

    assert len(result.cues) == 1

    cue = result.cues[0]

    assert cue.name == "Intro"

    assert cue.number == 1


def test_round_trip():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    original = create_capture_project()

    data = serializer.to_dict(
        original,
    )

    restored = loader.from_dict(
        data,
    )

    assert restored.name == original.name

    assert len(restored.fixtures) == len(original.fixtures)

    assert len(restored.universes) == len(original.universes)

    assert len(restored.cues) == len(original.cues)

    assert (
        restored.fixtures[0].name
        ==
        original.fixtures[0].name
    )

    assert (
        restored.universes[0].universe
        ==
        original.universes[0].universe
    )

    assert (
        restored.cues[0].number
        ==
        original.cues[0].number
    )


def test_load_file(tmp_path):

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    path = tmp_path / "capture_project.json"

    serializer.save(
        create_capture_project(),
        path,
    )

    result = loader.load(
        path,
    )

    assert result.name == "Recovered Capture"

    assert len(result) == 3