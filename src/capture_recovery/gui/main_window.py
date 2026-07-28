"""
Main graphical interface for Capture Recovery.
"""

from __future__ import annotations


from pathlib import Path


from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QSplitter,
    QTabWidget,
)


from capture_recovery.pipeline import (
    CaptureProjectPipeline,
)


from capture_recovery.formats import (
    CaptureBinaryStructureAnalyzer,
    CaptureBinaryObjectAnalyzer,
)


from capture_recovery.gui.binary_analysis_panel import (
    BinaryAnalysisPanel,
)


from capture_recovery.gui.object_analysis_panel import (
    ObjectAnalysisPanel,
)



class MainWindow(QMainWindow):
    """
    Main application window.
    """


    def __init__(
        self,
    ):

        super().__init__()


        self.pipeline = CaptureProjectPipeline()


        self.binary_analyzer = (
            CaptureBinaryStructureAnalyzer()
        )


        self.object_analyzer = (
            CaptureBinaryObjectAnalyzer()
        )


        self.current_project = None


        self.setWindowTitle(
            "Capture Recovery"
        )


        self.resize(
            1200,
            800,
        )


        self.file_label = QLabel(
            "Aucun fichier sélectionné"
        )


        self.open_button = QPushButton(
            "Ouvrir et analyser"
        )


        self.open_button.clicked.connect(
            self.open_file
        )


        self.tree = QTreeWidget()


        self.tree.setHeaderLabels(
            [
                "Projet",
                "Valeur",
            ]
        )


        self.log = QTextEdit()


        self.log.setReadOnly(
            True
        )


        self.binary_panel = (
            BinaryAnalysisPanel()
        )


        self.object_panel = (
            ObjectAnalysisPanel()
        )


        self.tabs = QTabWidget()


        project_widget = QWidget()


        project_layout = QVBoxLayout()


        project_layout.addWidget(
            self.file_label
        )


        project_layout.addWidget(
            self.open_button
        )


        project_layout.addWidget(
            self.tree
        )


        project_widget.setLayout(
            project_layout
        )


        self.tabs.addTab(
            project_widget,
            "Projet",
        )


        self.tabs.addTab(
            self.binary_panel,
            "Analyse binaire",
        )


        self.tabs.addTab(
            self.object_panel,
            "Objets",
        )


        right = QWidget()


        right_layout = QVBoxLayout()


        right_layout.addWidget(
            self.log
        )


        right.setLayout(
            right_layout
        )


        splitter = QSplitter()


        splitter.addWidget(
            self.tabs
        )


        splitter.addWidget(
            right
        )


        self.setCentralWidget(
            splitter
        )



    def open_file(
        self,
    ):

        filename, _ = QFileDialog.getOpenFileName(

            self,

            "Choisir un projet Capture",

            "",

            "Capture Projects (*.c2p *.c2 *.cap)",

        )


        if not filename:

            return


        path = Path(
            filename
        )


        self.file_label.setText(
            str(path)
        )


        self.tree.clear()


        self.binary_panel.clear()


        self.object_panel.clear()


        self.log.clear()


        self.log.append(
            "Analyse du projet..."
        )


        try:

            result = self.pipeline.process(
                path
            )


            self.current_project = result


            self.display_project(
                result
            )


            binary_result = (
                self.binary_analyzer.analyze(
                    path
                )
            )


            self.binary_panel.display_analysis(
                binary_result
            )


            object_result = (
                self.object_analyzer.analyze(
                    path
                )
            )


            self.object_panel.display_objects(
                object_result
            )


            self.log.append(
                "Analyse terminée."
            )


        except Exception as error:


            self.log.append(
                f"Erreur : {error}"
            )



    def display_project(
        self,
        result,
    ):


        self.tree.clear()


        project = result.get(
            "project",
            {},
        )


        root = QTreeWidgetItem(
            [
                "Projet",
                project.get(
                    "name",
                    "",
                ),
            ]
        )


        self.tree.addTopLevelItem(
            root
        )


        self.add_value(
            root,
            "Fichier",
            project.get(
                "file",
                "",
            ),
        )


        self.add_list(
            root,
            "Fixtures",
            project.get(
                "fixtures",
                [],
            ),
        )


        self.add_list(
            root,
            "Scenes",
            project.get(
                "scenes",
                [],
            ),
        )


        self.add_list(
            root,
            "Groups",
            project.get(
                "groups",
                [],
            ),
        )


        self.add_list(
            root,
            "Patch",
            project.get(
                "patch",
                [],
            ),
        )


        root.setExpanded(
            True
        )



    def add_value(
        self,
        parent,
        key,
        value,
    ):


        item = QTreeWidgetItem(
            [
                str(key),
                str(value),
            ]
        )


        parent.addChild(
            item
        )



    def add_list(
        self,
        parent,
        title,
        values,
    ):


        category = QTreeWidgetItem(
            [
                title,
                str(len(values)),
            ]
        )


        parent.addChild(
            category
        )


        for value in values[:100]:


            if isinstance(
                value,
                dict,
            ):


                name = value.get(
                    "name",
                    str(value),
                )


            else:

                name = str(value)



            item = QTreeWidgetItem(
                [
                    name,
                    "",
                ]
            )


            category.addChild(
                item
            )