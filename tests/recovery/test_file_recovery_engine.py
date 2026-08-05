from pathlib import Path


from capture_recovery.recovery import (
    FileRecoveryEngine,
)


from capture_recovery.reconstruction import (
    RecoveryOrchestrator,
)



def test_file_recovery_engine_missing_file(tmp_path):

    engine = FileRecoveryEngine(
        RecoveryOrchestrator()
    )


    missing = tmp_path / "missing.c2p"


    try:

        engine.recover_file(
            missing,

            missing,

            tmp_path / "out.c2p",

            object_type="fixture",
        )

    except FileNotFoundError:

        assert True

    else:

        assert False