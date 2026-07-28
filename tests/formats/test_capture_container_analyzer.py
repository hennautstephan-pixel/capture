from capture_recovery.formats import (
    CaptureContainerAnalyzer,
)


def test_capture_container_analyzer():

    analyzer = CaptureContainerAnalyzer()


    metadata = {

        "ascii_strings": [

            "Robe Pointe",
            "Universe 2",
            "Scene Intro",
            "Group Actors",

        ],

        "utf16_strings": [],

    }


    result = analyzer.analyze(
        metadata
    )


    assert len(
        result["fixtures"]
    ) == 1


    assert result["universes"][0]["universe"] == 2


    assert len(
        result["scenes"]
    ) == 1


    assert len(
        result["groups"]
    ) == 1