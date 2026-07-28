import sys

import pytest

from PySide6.QtWidgets import QApplication


from capture_recovery.gui.object_analysis_panel import (
    ObjectAnalysisPanel,
)



@pytest.fixture
def app():

    application = QApplication.instance()


    if application is None:

        application = QApplication(
            sys.argv
        )


    return application



def test_object_analysis_panel(
    app,
):

    panel = ObjectAnalysisPanel()


    analysis = {

        "count": 1,

        "objects": [

            {
                "offset": 64,

                "size": 128,

                "confidence": 0.8,

            }

        ],

    }


    panel.display_objects(
        analysis
    )


    assert (
        panel.tree.topLevelItemCount()
        == 1
    )