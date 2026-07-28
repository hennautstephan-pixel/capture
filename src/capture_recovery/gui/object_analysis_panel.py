"""
Object analysis panel.

Displays detected binary object
candidates from Capture projects.
"""

from __future__ import annotations


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
)



class ObjectAnalysisPanel(QWidget):
    """
    Display detected binary objects.
    """


    MAX_ITEMS = 200



    def __init__(
        self,
        parent=None,
    ):

        super().__init__(
            parent
        )


        self.title = QLabel(
            "Objets détectés"
        )


        self.tree = QTreeWidget()


        self.tree.setHeaderLabels(
            [
                "Élément",
                "Valeur",
            ]
        )


        layout = QVBoxLayout()


        layout.addWidget(
            self.title
        )


        layout.addWidget(
            self.tree
        )


        self.setLayout(
            layout
        )



    def clear(
        self,
    ):

        self.tree.clear()



    def display_objects(
        self,
        analysis: dict,
    ):
        """
        Display detected objects.
        """


        self.tree.clear()


        root = QTreeWidgetItem(
            [
                "Objets",
                str(
                    analysis.get(
                        "count",
                        0,
                    )
                ),
            ]
        )


        self.tree.addTopLevelItem(
            root
        )


        objects = analysis.get(
            "objects",
            [],
        )


        for obj in objects[:self.MAX_ITEMS]:


            offset = obj.get(
                "offset",
                0,
            )


            size = obj.get(
                "size",
                0,
            )


            confidence = obj.get(
                "confidence",
                0,
            )


            item = QTreeWidgetItem(
                [
                    f"0x{offset:X}",
                    (
                        f"Taille={size} "
                        f"Confiance={confidence}"
                    ),
                ]
            )


            root.addChild(
                item
            )


        root.setExpanded(
            True
        )