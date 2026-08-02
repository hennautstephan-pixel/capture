from pathlib import Path

from capture_recovery.knowledge import (
    CaptureFormatBuilder,
)


def test_missing_directory():

    builder = CaptureFormatBuilder()

    try:
        builder.build("directory_that_does_not_exist")
        assert False
    except FileNotFoundError:
        pass


def test_empty_directory(tmp_path: Path):

    builder = CaptureFormatBuilder()

    fmt = builder.build(tmp_path)

    assert fmt.statistics()["field_count"] == 0


def test_build_from_samples():

    samples = Path("samples")

    if not samples.exists():
        return

    builder = CaptureFormatBuilder()

    fmt = builder.build(samples)

    stats = fmt.statistics()

    assert stats["field_count"] > 0

    project = fmt.get("Project")

    assert project is not None
    assert project.confidence == 1.0

    software = fmt.get("SoftwareVersion")

    assert software is not None
    assert software.confidence == 1.0


def test_fields_are_sorted():

    samples = Path("samples")

    if not samples.exists():
        return

    builder = CaptureFormatBuilder()

    fmt = builder.build(samples)

    offsets = [
        field.offset
        for field in fmt.all_fields()
    ]

    assert offsets == sorted(offsets)