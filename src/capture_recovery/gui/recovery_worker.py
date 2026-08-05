"""
Recovery worker.

Runs file recovery in a background Qt thread
to keep the GUI responsive.
"""

from __future__ import annotations


from pathlib import Path


from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)


from capture_recovery.recovery.file_recovery_engine import (
    FileRecoveryEngine,
)



class RecoveryWorker(QObject):
    """
    Background recovery worker.

    The worker executes FileRecoveryEngine
    outside the GUI thread.
    """


    # ---------------------------------------------------------
    # Signals
    # ---------------------------------------------------------

    finished = Signal(
        object,
    )


    error = Signal(
        str,
    )


    progress = Signal(
        str,
    )


    # ---------------------------------------------------------
    # Init
    # ---------------------------------------------------------

    def __init__(
        self,
        engine: FileRecoveryEngine,
        source: Path,
        reference: Path,
        output: Path,
        object_type: str = "fixture",
    ) -> None:

        super().__init__()

        self.engine = engine

        self.source = source

        self.reference = reference

        self.output = output

        self.object_type = object_type



    # ---------------------------------------------------------
    # Execution
    # ---------------------------------------------------------

    @Slot()
    def run(
        self,
    ) -> None:
        """
        Execute recovery.
        """

        try:

            self.progress.emit(
                "Lecture des fichiers..."
            )


            result = self.engine.recover_file(
                self.source,
                self.reference,
                self.output,
                object_type=self.object_type,
            )


            self.progress.emit(
                "Validation terminée."
            )


            self.finished.emit(
                result,
            )


        except Exception as exc:

            self.error.emit(
                str(exc),
            )