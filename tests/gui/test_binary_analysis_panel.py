import sys

import pytest

from PySide6.QtWidgets import QApplication

from capture_recovery.gui.binary_analysis_panel import (
    BinaryAnalysisPanel,
)



@pytest.fixture
def app():

    application = QApplication.instance()

    if application is None:

        application = QApplication(
            sys.argv
        )

    return application



def test_binary_analysis_panel(
    app,
):

    panel = BinaryAnalysisPanel()


    analysis = {

        "file": "project.c2p",

        "size": 100,

        "sha256": "abc",

        "entropy": 3.2,

        "ascii_strings": [

            {
                "offset": 0,
                "value": "Project",
            }

        ],

        "utf16_strings": [],

        "blocks": [],

    }


    panel.display_analysis(
        analysis
    )


    assert (
        panel.tree.topLevelItemCount()
        == 1
    )