from pathlib import Path

from capture_recovery.research import CorpusBuilder


def test_builder_empty_directory(tmp_path):

    builder = CorpusBuilder()

    database, result = builder.build(
        tmp_path,
    )

    assert result.sample_count == 0
    assert result.comparison_count == 0
    assert result.knowledge_count == 0
    assert database.samples() == ()