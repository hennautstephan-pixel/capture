"""
Binary analysis panel.

Displays low level Capture project
binary structure information.
"""

from __future__ import annotations


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
)



class BinaryAnalysisPanel(QWidget):
    """
    Display binary analysis results.
    """



    MAX_ITEMS = 50



    def __init__(
        self,
        parent=None,
    ):

        super().__init__(
            parent
        )


        self.title = QLabel(
            "Analyse binaire"
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



    def display_analysis(
        self,
        analysis: dict,
    ):
        """
        Display binary analyzer result.
        """


        self.tree.clear()


        root = QTreeWidgetItem(
            [
                "Analyse",
                "",
            ]
        )


        self.tree.addTopLevelItem(
            root
        )


        self._add_value(
            root,
            "Fichier",
            analysis.get(
                "file",
                "",
            ),
        )


        self._add_value(
            root,
            "Taille",
            f"{analysis.get('size', 0)} octets",
        )


        self._add_value(
            root,
            "SHA256",
            analysis.get(
                "sha256",
                "",
            ),
        )


        self._add_value(
            root,
            "Entropie",
            analysis.get(
                "entropy",
                0,
            ),
        )


        self._add_list(
            root,
            "Chaînes ASCII",
            analysis.get(
                "ascii_strings",
                [],
            ),
        )


        self._add_list(
            root,
            "Chaînes UTF16",
            analysis.get(
                "utf16_strings",
                [],
            ),
        )


        self._add_list(
            root,
            "Blocs binaires",
            analysis.get(
                "blocks",
                [],
            ),
        )


        root.setExpanded(
            True
        )



    def _add_value(
        self,
        parent,
        key,
        value,
    ):

        item = QTreeWidgetItem(
            [
                str(key),
                str(value)[:300],
            ]
        )


        parent.addChild(
            item
        )



    def _add_list(
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


        for value in values[:self.MAX_ITEMS]:


            if isinstance(
                value,
                dict,
            ):

                if "offset" in value:

                    text = (
                        f"0x{value['offset']:X} : "
                        f"{value.get('value', value)}"
                    )

                else:

                    text = str(
                        value
                    )

            else:

                text = str(
                    value
                )


            item = QTreeWidgetItem(
                [
                    text[:150],
                    "",
                ]
            )


            category.addChild(
                item
            )


        if len(values) > self.MAX_ITEMS:

            remaining = QTreeWidgetItem(
                [
                    "...",
                    f"{len(values)-self.MAX_ITEMS} éléments masqués",
                ]
            )

            category.addChild(
                remaining
            )