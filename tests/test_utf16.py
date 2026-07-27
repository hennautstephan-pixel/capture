from src.capture_recovery.binary_reader import BinaryReader
from src.capture_recovery.analyzers.utf16 import Utf16Analyzer
from src.capture_recovery.models import Report


def test_utf16(tmp_path):

    filename = tmp_path / "utf16.bin"

    filename.write_bytes(
        "Bonjour".encode("utf-16le")
    )

    with BinaryReader(filename) as reader:

        report = Report(
            filename="utf16.bin",
            filesize=reader.size,
        )

        Utf16Analyzer().run(reader, report)

        assert len(report.findings) == 1
        assert report.findings[0].value == "Bonjour"