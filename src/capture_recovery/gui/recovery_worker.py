from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from capture_recovery import recover


class RecoveryWorker(QObject):

    progress = Signal(str)

    finished = Signal(dict)

    error = Signal(str)


    def __init__(
        self,
        path,
    ):
        super().__init__()

        self.path = path


    @Slot()
    def run(self):

        try:

            self.progress.emit(
                "Analyse du fichier..."
            )


            result = recover(
                self.path,
            )


            self.progress.emit(
                "Reconstruction terminée"
            )


            self.finished.emit(
                result
            )


        except Exception as e:

            self.error.emit(
                str(e)
            )