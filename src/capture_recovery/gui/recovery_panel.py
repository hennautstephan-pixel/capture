# src/capture_recovery/gui/recovery_panel.py

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QMessageBox,
)

from capture_recovery.recovery.file_recovery_engine import (
    FileRecoveryEngine,
)

from capture_recovery.reconstruction import (
    RecoveryOrchestrator,
    ReconstructionStrategy,
)

from capture_recovery.reconstruction.object_library import (
    ObjectLibrary,
)

from capture_recovery.gui.recovery_worker import (
    RecoveryWorker,
)


class RecoveryPanel(QWidget):

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.engine = None

        self.thread = None
        self.worker = None

        self._build_ui()


    # ==========================================================
    # Engine creation
    # ==========================================================

    def _build_engine(
        self,
        reference_file: Path,
    ) -> FileRecoveryEngine:

        from capture_recovery.research.reference_project_analyzer import (
            ReferenceProjectAnalyzer,
        )

        from capture_recovery.research.reference_object_extractor import (
            ReferenceObjectExtractor,
        )

        from capture_recovery.research.reference_library_builder import (
            ReferenceLibraryBuilder,
        )


        self.report.append(
            "Analyse du projet référence..."
        )


        analyzer = ReferenceProjectAnalyzer()

        project_model = analyzer.analyze(
            reference_file,
        )


        self.report.append(
            f"Blocs référence : {len(project_model.blocks)}"
        )


        extractor = ReferenceObjectExtractor(
            object_type="fixture",
        )


        objects = extractor.extract(
            project_model,
        )


        self.report.append(
            f"Objets extraits : {len(objects)}"
        )


        builder = ReferenceLibraryBuilder()

        result = builder.build(
            objects,
        )


        library = result.library


        self.report.append(
            f"Bibliothèque : {library.size} objets"
        )


        strategy = ReconstructionStrategy(
            library,
        )


        orchestrator = RecoveryOrchestrator(
            strategy=strategy,
        )


        return FileRecoveryEngine(
            orchestrator,
        )


    # ==========================================================
    # UI
    # ==========================================================

    def _build_ui(
        self,
    ):

        layout = QVBoxLayout(
            self,
        )


        self.source_edit = self._create_path_row(
            layout,
            "Fichier corrompu",
            self.select_source,
        )


        self.reference_edit = self._create_path_row(
            layout,
            "Fichier référence",
            self.select_reference,
        )


        self.output_edit = self._create_path_row(
            layout,
            "Fichier récupéré",
            self.select_output,
        )


        self.recover_button = QPushButton(
            "Lancer la récupération",
        )


        self.recover_button.clicked.connect(
            self.recover,
        )


        layout.addWidget(
            self.recover_button,
        )


        layout.addWidget(
            QLabel(
                "Rapport",
            )
        )


        self.report = QTextEdit()

        self.report.setReadOnly(
            True,
        )


        layout.addWidget(
            self.report,
        )


    def _create_path_row(
        self,
        layout,
        title,
        callback,
    ):

        row = QHBoxLayout()

        label = QLabel(title)

        edit = QLineEdit()

        button = QPushButton(
            "...",
        )

        button.clicked.connect(
            callback,
        )

        row.addWidget(label)
        row.addWidget(edit)
        row.addWidget(button)

        layout.addLayout(
            row,
        )

        return edit


    # ==========================================================
    # File selection
    # ==========================================================

    def select_source(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir fichier corrompu",
            "",
            "Capture (*.c2p *.cap *.c2)",
        )

        if filename:
            self.source_edit.setText(
                filename,
            )


    def select_reference(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir référence",
            "",
            "Capture (*.c2p *.cap *.c2)",
        )

        if filename:
            self.reference_edit.setText(
                filename,
            )


    def select_output(self):

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Créer récupération",
            "",
            "Capture (*.c2p)",
        )

        if filename:
            self.output_edit.setText(
                filename,
            )


    # ==========================================================
    # Recovery
    # ==========================================================

    def recover(self):

        if self.thread is not None:

            return


        source = Path(
            self.source_edit.text(),
        )

        reference = Path(
            self.reference_edit.text(),
        )

        output = Path(
            self.output_edit.text(),
        )


        if not source.exists():

            QMessageBox.warning(
                self,
                "Erreur",
                "Fichier corrompu absent.",
            )

            return


        if not reference.exists():

            QMessageBox.warning(
                self,
                "Erreur",
                "Fichier référence absent.",
            )

            return


        if not self.output_edit.text():

            QMessageBox.warning(
                self,
                "Erreur",
                "Choisissez un fichier de sortie.",
            )

            return


        self.report.clear()


        try:

            self.engine = self._build_engine(
                reference,
            )


        except Exception as error:

            QMessageBox.critical(
                self,
                "Erreur bibliothèque",
                str(error),
            )

            return


        self.recover_button.setEnabled(
            False,
        )


        self.thread = QThread()


        self.worker = RecoveryWorker(
            self.engine,
            source,
            reference,
            output,
            "fixture",
        )


        self.worker.moveToThread(
            self.thread,
        )


        self.thread.started.connect(
            self.worker.run,
        )


        self.worker.progress.connect(
            self.report.append,
        )


        self.worker.finished.connect(
            self.on_finished,
        )


        self.worker.error.connect(
            self.on_error,
        )


        self.worker.finished.connect(
            self.thread.quit,
        )


        self.worker.error.connect(
            self.thread.quit,
        )


        self.thread.finished.connect(
            self.cleanup_thread,
        )


        self.thread.start()



    def on_finished(
        self,
        result,
    ):

        self.report.append(
            ""
        )

        self.report.append(
            f"Succès : {result.success}"
        )

        self.report.append(
            f"Réparations : {result.repaired_regions}"
        )

        self.report.append(
            f"Validation : {result.validation.valid}"
        )

        self.recover_button.setEnabled(
            True,
        )


    def on_error(
        self,
        message,
    ):

        self.report.append(
            f"Erreur : {message}"
        )

        self.recover_button.setEnabled(
            True,
        )


    def cleanup_thread(self):

        if self.worker:
            self.worker.deleteLater()

        if self.thread:
            self.thread.deleteLater()


        self.worker = None
        self.thread = None