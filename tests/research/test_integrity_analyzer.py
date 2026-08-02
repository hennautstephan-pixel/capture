from __future__ import annotations

from capture_recovery.research import (
    CandidateObject,
    FieldCorrelation,
    IntegrityAnalyzer,
    IntegrityReport,
    IntegritySeverity,
    LayoutRegion,
    ObjectMap,
    ProjectLayout,
    ProjectLayoutBuilder,
    RegionKind,
)


def create_object(
    offset: int,
    length: int,
):

    field = FieldCorrelation(
        offset=offset,
        length=length,
        confidence=1.0,
        type_candidates=("bytes",),
        evidence=("test",),
        occurrence_count=1,
    )

    return CandidateObject(
        offset=offset,
        length=length,
        confidence=1.0,
        fields=(field,),
    )


def create_layout():

    builder = ProjectLayoutBuilder()

    return builder.build(
        file_size=200,
        header_size=20,
        stream_offset=20,
        stream_length=160,
        footer_size=20,
        objects=ObjectMap(
            [
                create_object(
                    40,
                    20,
                )
            ]
        ),
    )


def test_valid_layout():

    analyzer = IntegrityAnalyzer()

    report = analyzer.analyze(
        create_layout()
    )

    assert isinstance(
        report,
        IntegrityReport,
    )

    assert report.valid


def test_zero_length_region():

    layout = create_layout()

    layout = ProjectLayout(
        header=LayoutRegion(
            0,
            0,
            RegionKind.HEADER,
            1.0,
        ),
        stream=layout.stream,
        footer=layout.footer,
        objects=layout.objects,
        gaps=layout.gaps,
    )

    report = (
        IntegrityAnalyzer()
        .analyze(layout)
    )

    assert not report.valid

    assert report.error_count == 1


def test_object_outside_stream():

    builder = ProjectLayoutBuilder()

    layout = builder.build(
        file_size=200,
        header_size=20,
        stream_offset=20,
        stream_length=160,
        footer_size=20,
        objects=ObjectMap(
            [
                create_object(
                    190,
                    20,
                )
            ]
        ),
    )

    report = (
        IntegrityAnalyzer()
        .analyze(layout)
    )

    assert report.error_count == 1


def test_score():

    report = (
        IntegrityAnalyzer()
        .analyze(
            create_layout()
        )
    )

    assert 0.0 <= report.score <= 1.0


def test_counts():

    report = (
        IntegrityAnalyzer()
        .analyze(
            create_layout()
        )
    )

    assert report.error_count == 0

    assert report.warning_count == 0

    assert report.info_count == 0


def test_severity():

    report = (
        IntegrityAnalyzer()
        .analyze(
            create_layout()
        )
    )

    for issue in report.issues:

        assert isinstance(
            issue.severity,
            IntegritySeverity,
        )