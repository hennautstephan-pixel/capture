from capture_recovery.formats import (
    CaptureProjectBuilder,
)

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from capture_recovery.models.project import (
    Project,
)


def create_fixture():

    return SemanticObject(
        object_type="Fixture",
        identifier="MAC Aura",
        properties={
            "manufacturer": "Martin",
            "model": "MAC Aura",
            "universe": 1,
            "address": 10,
        },
    )


def create_universe():

    return SemanticObject(
        object_type="Universe",
        identifier="Universe 1",
        properties={
            "universe": 1,
            "protocol": "sACN",
            "priority": 100,
            "ip_address": "2.0.0.1",
            "port": 5568,
        },
    )


def create_cue():

    return SemanticObject(
        object_type="Cue",
        identifier="Intro",
        properties={
            "cue_number": 1,
            "fade": 3.0,
        },
    )


def create_project():

    project = Project(
        name="Complete Test",
    )

    project.add(
        create_fixture(),
    )

    project.add(
        create_universe(),
    )

    project.add(
        create_cue(),
    )

    return project


def test_build_complete_capture_project():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    assert result.name == (
        "Complete Test"
    )


def test_builds_universe():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.universes
    ) == 1

    assert result.universes[0].universe == 1


def test_builds_cue():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.cues
    ) == 1

    assert result.cues[0].name == (
        "Intro"
    )


def test_fixture_requires_builder():

    builder = CaptureProjectBuilder()

    result = builder.build(
        create_project(),
    )

    assert len(
        result.fixtures
    ) == 0