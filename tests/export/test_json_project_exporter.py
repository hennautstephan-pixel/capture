from capture_recovery.export.json_project_exporter import (
    JsonProjectExporter,
)
from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)
from capture_recovery.models.project import Project


def create_project():

    project = Project(
        name="Recovered Capture",
    )

    project.add(
        SemanticObject(
            object_type="Fixture",
            identifier="Mac Aura",
            properties={
                "manufacturer": "Martin",
            },
            confidence=1.0,
        )
    )

    project.add(
        SemanticObject(
            object_type="Universe",
            identifier="Universe 1",
            properties={
                "universe": 1,
            },
            confidence=0.9,
        )
    )

    return project


def test_export_dict():

    exporter = JsonProjectExporter()

    data = exporter.export_dict(
        create_project(),
    )

    assert data["name"] == "Recovered Capture"

    assert len(data["objects"]) == 2

    assert data["objects"][0]["type"] == "Fixture"


def test_export_string():

    exporter = JsonProjectExporter()

    result = exporter.export_string(
        create_project(),
    )

    assert isinstance(
        result,
        str,
    )

    assert "Mac Aura" in result


def test_export_file(tmp_path):

    exporter = JsonProjectExporter()

    target = tmp_path / "project.json"

    exporter.export_file(
        create_project(),
        target,
    )

    assert target.exists()

    content = target.read_text(
        encoding="utf-8",
    )

    assert "Recovered Capture" in content