import sys


import pytest


from PySide6.QtWidgets import QApplication


from capture_recovery.gui.signature_analysis_panel import (
    SignatureAnalysisPanel,
)



@pytest.fixture
def app():

    application = QApplication.instance()


    if application is None:

        application = QApplication(
            sys.argv
        )


    return application



def test_signature_analysis_panel(
    app,
):


    panel = SignatureAnalysisPanel()



    panel.display_signatures(

        {

            "signature_count": 1,

            "signatures": [

                {

                    "occurrences": 4,

                    "size": 32,

                    "offsets": [

                        64,

                        128,

                    ],

                }

            ],

        }

    )


    assert (
        panel.tree.topLevelItemCount()
        == 1
    )