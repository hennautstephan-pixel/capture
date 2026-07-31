from pathlib import Path

from capture_recovery.benchmark import (
    BenchmarkAnalyser,
    BenchmarkReport,
    BenchmarkRunner,
    SampleLoader,
)


def main() -> None:

    samples = Path("samples")

    if not samples.exists():
        print("Le dossier 'samples' est introuvable.")
        return

    loader = SampleLoader(samples)

    runner = BenchmarkRunner(
        loader,
        BenchmarkAnalyser(),
    )

    print("=" * 60)
    print("Capture Recovery Benchmark")
    print("=" * 60)
    print()

    session = runner.run_session()

    report = BenchmarkReport(
        session.statistics,
    )

    print(report.to_text())


if __name__ == "__main__":
    main()