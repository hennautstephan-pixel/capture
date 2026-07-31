from capture_recovery.analysis import AnalysisResult
from capture_recovery.benchmark import BenchmarkAnalyser


class FakePipeline:

    def analyse(
        self,
        path: str,
    ) -> AnalysisResult:

        return AnalysisResult(
            filename=path,
            file_size=2048,
            object_count=100,
            property_count=250,
            candidate_count=180,
            average_confidence=0.91,
            minimum_confidence=0.72,
            maximum_confidence=1.00,
            unknown_objects=8,
            unknown_signatures=3,
            conflict_count=2,
            duration_seconds=0.42,
        )


def test_pipeline_property():

    analyser = BenchmarkAnalyser(
        FakePipeline(),
    )

    assert analyser.pipeline is not None


def test_call():

    analyser = BenchmarkAnalyser(
        FakePipeline(),
    )

    result = analyser(
        "demo.c2p",
    )

    assert result.filename == "demo.c2p"

    assert result.file_size == 2048

    assert result.object_count == 100

    assert result.recovered_objects == 92

    assert result.unknown_objects == 8

    assert result.property_count == 250

    assert result.candidate_count == 180

    assert result.average_confidence == 0.91

    assert result.minimum_confidence == 0.72

    assert result.maximum_confidence == 1.00

    assert result.conflict_count == 2

    assert result.unknown_signature_count == 3

    assert result.duration_seconds == 0.42