from capture_recovery.knowledge import (
    CaptureField,
    CaptureFormat,
)


def test_empty_format():

    fmt = CaptureFormat()

    assert fmt.all_fields() == ()


def test_add_field():

    fmt = CaptureFormat()

    field = CaptureField(
        name="Project",
        offset=4,
        size=8,
        confidence=1.0,
    )

    fmt.add_field(field)

    assert fmt.get("Project") == field


def test_unknown_field():

    fmt = CaptureFormat()

    assert fmt.get("Unknown") is None


def test_fields_are_sorted_by_offset():

    fmt = CaptureFormat()

    fmt.add_field(
        CaptureField(
            name="Second",
            offset=20,
            size=4,
            confidence=1.0,
        )
    )

    fmt.add_field(
        CaptureField(
            name="First",
            offset=4,
            size=4,
            confidence=1.0,
        )
    )

    fields = fmt.all_fields()

    assert len(fields) == 2
    assert fields[0].name == "First"
    assert fields[1].name == "Second"


def test_statistics_empty():

    fmt = CaptureFormat()

    stats = fmt.statistics()

    assert stats["field_count"] == 0
    assert stats["average_confidence"] == 0.0


def test_statistics():

    fmt = CaptureFormat()

    fmt.add_field(
        CaptureField(
            name="A",
            offset=0,
            size=4,
            confidence=1.0,
        )
    )

    fmt.add_field(
        CaptureField(
            name="B",
            offset=4,
            size=8,
            confidence=0.5,
        )
    )

    stats = fmt.statistics()

    assert stats["field_count"] == 2
    assert stats["average_confidence"] == 0.75


def test_default_contains_project():

    fmt = CaptureFormat.default()

    field = fmt.get("Project")

    assert field is not None
    assert field.offset == 0x0004
    assert field.size == 8
    assert field.confidence == 1.0
    assert field.metadata["encoding"] == "ascii"
    assert field.metadata["value"] == "Project"


def test_default_contains_software_version():

    fmt = CaptureFormat.default()

    field = fmt.get("SoftwareVersion")

    assert field is not None
    assert field.offset == 0x0014
    assert field.size == 16
    assert field.confidence == 1.0
    assert field.metadata["encoding"] == "ascii"
    assert field.metadata["value"] == "SoftwareVersion"


def test_default_fields_are_sorted():

    fmt = CaptureFormat.default()

    fields = fmt.all_fields()

    offsets = [field.offset for field in fields]

    assert offsets == sorted(offsets)