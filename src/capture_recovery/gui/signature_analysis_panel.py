"""
Signature analysis panel.

Displays repeated binary signatures
found in Capture project files.
"""

from __future__ import annotations


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
)



class SignatureAnalysisPanel(QWidget):
    """
    Display binary signature analysis.
    """



    MAX_SIGNATURES = 100

    MAX_OFFSETS = 20



    def __init__(
        self,
        parent=None,
    ):

        super().__init__(
            parent
        )


        self.title = QLabel(
            "Signatures détectées"
        )


        self.tree = QTreeWidget()


        self.tree.setHeaderLabels(
            [
                "Signature",
                "Informations",
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



    def display_signatures(
        self,
        analysis: dict,
    ):
        """
        Display signature analysis.
        """


        self.tree.clear()


        signatures = analysis.get(
            "signatures",
            [],
        )


        root = QTreeWidgetItem(
            [
                "Total signatures",
                str(
                    analysis.get(
                        "signature_count",
                        len(signatures),
                    )
                ),
            ]
        )


        self.tree.addTopLevelItem(
            root
        )



        for index, signature in enumerate(
            signatures[:self.MAX_SIGNATURES],
            start=1,
        ):


            item = QTreeWidgetItem(
                [
                    f"#{index}",
                    (
                        f"Occurrences="
                        f"{signature.get('occurrences', 0)} "
                        f"Taille="
                        f"{signature.get('size', 0)}"
                    ),
                ]
            )


            root.addChild(
                item
            )



            offsets = signature.get(
                "offsets",
                [],
            )


            for offset in offsets[:self.MAX_OFFSETS]:


                child = QTreeWidgetItem(
                    [
                        "Offset",
                        f"0x{offset:X}",
                    ]
                )


                item.addChild(
                    child
                )


        root.setExpanded(
            True
        )