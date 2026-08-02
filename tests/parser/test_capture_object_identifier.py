from capture_recovery.parser import (
    CandidateKind,
    IdentificationReport,
    ObjectCollection,
    ObjectIdentifier,
    ParsedObject,
)


def test_empty():

    report = ObjectIdentifier().identify(
        ObjectCollection(objects=())
    )

    assert isinstance(
        report,
        IdentificationReport,
    )

    assert report.count == 0


def test_binary():

    collection = ObjectCollection(
        objects=(
            ParsedObject(
                offset=0,
                size=4,
                raw=b"\x00\x01\x02\x03",
            ),
        )
    )

    report = ObjectIdentifier().identify(
        collection,
    )

    assert report.count == 1

    assert (
        report.objects[0].kind
        is CandidateKind.BINARY
    )


def test_text():

    collection = ObjectCollection(
        objects=(
            ParsedObject(
                offset=0,
                size=11,
                raw=b"Hello World",
            ),
        )
    )

    report = ObjectIdentifier().identify(
        collection,
    )

    assert (
        report.objects[0].kind
        is CandidateKind.TEXT
    )