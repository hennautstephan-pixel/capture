from pathlib import Path


from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
)


from PySide6.QtCore import (
    QThread,
)


from .recovery_worker import (
    RecoveryWorker,
)



class MainWindow(QMainWindow):


    def __init__(self):

        super().__init__()


        self.setWindowTitle(
            "Capture Recovery"
        )


        self.resize(
            900,
            600,
        )


        self.file_label = QLabel(
            "Aucun fichier sélectionné"
        )


        self.log = QTextEdit()

        self.log.setReadOnly(
            True
        )


        self.button = QPushButton(
            "Ouvrir et récupérer"
        )


        self.button.clicked.connect(
            self.open_file
        )


        layout = QVBoxLayout()


        layout.addWidget(
            self.file_label
        )


        layout.addWidget(
            self.button
        )


        layout.addWidget(
            self.log
        )


        widget = QWidget()

        widget.setLayout(
            layout
        )


        self.setCentralWidget(
            widget
        )



    def open_file(
        self,
    ):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir un projet Capture",
            "",
            "Capture (*.cap *.c2)",
        )


        if not file:
            return


        self.file_label.setText(
            file
        )


        self.thread = QThread()


        self.worker = RecoveryWorker(
            Path(file)
        )


        self.worker.moveToThread(
            self.thread
        )


        self.thread.started.connect(
            self.worker.run
        )


        self.worker.progress.connect(
            self.log.append
        )


        self.worker.finished.connect(
            self.finished
        )


        self.worker.error.connect(
            self.log.append
        )


        self.thread.start()



    def finished(
        self,
        result,
    ):

        self.log.append(
            "Projet récupéré"
        )


        self.log.append(
            str(result)
        )