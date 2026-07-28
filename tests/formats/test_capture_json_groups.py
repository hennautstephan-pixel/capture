from capture_recovery.formats import (
    CaptureGroup,
    CaptureJsonLoader,
    CaptureJsonSerializer,
    CaptureProject,
)


def create_project():

    project = CaptureProject(
        name="Group JSON Test",
    )

    project.add_group(
        CaptureGroup(
            name="Face",
            fixtures=[
                "MAC Aura 1",
                "MAC Aura 2",
            ],
            properties={
                "type": "front",
            },
        )
    )

    return project


def test_json_serializer_exports_groups():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    assert "groups" in result

    assert len(
        result["groups"],
    ) == 1


def test_json_serializer_exports_group_data():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    group = result["groups"][0]

    assert group["name"] == "Face"

    assert group["fixtures"] == [
        "MAC Aura 1",
        "MAC Aura 2",
    ]


def test_json_serializer_exports_group_properties():

    serializer = CaptureJsonSerializer()

    result = serializer.serialize(
        create_project(),
    )

    group = result["groups"][0]

    assert group["properties"]["type"] == (
        "front"
    )


def test_json_loader_restores_groups():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    data = serializer.serialize(
        create_project(),
    )

    result = loader.from_dict(
        data,
    )

    assert len(
        result.groups,
    ) == 1

    group = result.groups[0]

    assert group.name == "Face"

    assert group.fixtures == [
        "MAC Aura 1",
        "MAC Aura 2",
    ]


def test_json_group_round_trip():

    serializer = CaptureJsonSerializer()

    loader = CaptureJsonLoader()

    original = create_project()

    restored = loader.from_dict(
        serializer.to_dict(
            original,
        )
    )

    assert restored.name == (
        original.name
    )

    assert len(
        restored.groups,
    ) == len(
        original.groups,
    )

    assert restored.groups[0].name == (
        original.groups[0].name
    )