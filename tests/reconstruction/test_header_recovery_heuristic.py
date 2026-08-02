import pytest

from capture_recovery.reconstruction import (
    HeaderRecoveryHeuristic,
    HeaderScanner,
    HeaderSignature,
    ReconstructionContext,
)


def make_scanner():

    scanner = HeaderScanner()

    scanner.register(
        HeaderSignature(
            name="HDR",
            pattern=b"\xCA\xFE\xBA\xBE",
        )
    )

    return scanner


def test_supports_empty():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b""
    )

    assert not heuristic.supports(context)


def test_supports_non_empty():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\x00"
    )

    assert heuristic.supports(context)


def test_no_header():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\x00\x11\x22"
    )

    candidates = list(
        heuristic.reconstruct(context)
    )

    assert candidates == []


def test_single_header():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\x00\xCA\xFE\xBA\xBE\x11"
    )

    candidates = list(
        heuristic.reconstruct(context)
    )

    assert len(candidates) == 1

    candidate = candidates[0]

    assert candidate.score == 1.0

    assert (
        candidate.modifications["header_offset"]
        == 1
    )


def test_multiple_headers():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=(
            b"\xCA\xFE\xBA\xBE"
            b"\x00"
            b"\xCA\xFE\xBA\xBE"
        )
    )

    candidates = list(
        heuristic.reconstruct(context)
    )

    assert len(candidates) == 2


def test_alignment_bonus():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=(
            b"\xCA\xFE\xBA\xBE"
            b"\x00\x00\x00"
        )
    )

    candidate = list(
        heuristic.reconstruct(context)
    )[0]

    assert candidate.score == 1.0


def test_candidate_description():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\xCA\xFE\xBA\xBE"
    )

    candidate = list(
        heuristic.reconstruct(context)
    )[0]

    assert "Recovered header" in candidate.description


def test_candidate_metadata():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\x00\xCA\xFE\xBA\xBE"
    )

    candidate = list(
        heuristic.reconstruct(context)
    )[0]

    assert "alignment" in candidate.metadata


def test_candidate_size():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\xCA\xFE\xBA\xBE"
    )

    candidate = list(
        heuristic.reconstruct(context)
    )[0]

    assert (
        candidate.modifications["header_size"]
        == 4
    )


def test_candidate_name():

    heuristic = HeaderRecoveryHeuristic(
        make_scanner()
    )

    context = ReconstructionContext(
        data=b"\xCA\xFE\xBA\xBE"
    )

    candidate = list(
        heuristic.reconstruct(context)
    )[0]

    assert (
        candidate.modifications["header_name"]
        == "HDR"
    )