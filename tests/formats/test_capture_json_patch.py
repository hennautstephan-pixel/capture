from capture_recovery.formats import (
    CaptureJsonSerializer,
    CapturePatch,
    CaptureProject,
    PatchEntry,
)


def create_project():

    patch = CapturePatch()

    patch.add(
        PatchEntry(
            fixture="MAC Aura",
            universe=1,
            address=10,
            mode="Standard",
            channels=20,
            properties={
                "manufacturer": "Martin",
                "model": "MAC Aura",
            },
        )
    )

    project = CaptureProject(
        name="Patch JSON Test",
    )

    project.patch = patch

    return project


def test_json_serializer_exports_patch():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert "patch" in result

    assert "entries" in result["patch"]


def test_json_serializer_exports_patch_entry():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    entry = (
        result["patch"]["entries"][0]
    )

    assert entry["fixture"] == (
        "MAC Aura"
    )

    assert entry["universe"] == 1

    assert entry["address"] == 10

    assert entry["mode"] == (
        "Standard"
    )


def test_json_serializer_exports_patch_channels():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    entry = (
        result["patch"]["entries"][0]
    )

    assert entry["channels"] == 20


def test_json_serializer_exports_patch_properties():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    entry = (
        result["patch"]["entries"][0]
    )

    assert entry["properties"][
        "manufacturer"
    ] == "Martin"

    assert entry["properties"][
        "model"
    ] == "MAC Aura"


def test_empty_patch_is_serialized():

    serializer = CaptureJsonSerializer()

    project = CaptureProject(
        name="Empty Patch",
    )

    result = serializer.serialize(
        project,
    )

    assert result["patch"] == {
        "entries": [],
    }