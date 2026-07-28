"""
Capture container analyzer.

Extracts semantic information from
raw Capture project metadata.
"""

from __future__ import annotations

import re


class CaptureContainerAnalyzer:
    """
    Analyze extracted Capture container data.
    """


    FIXTURE_KEYWORDS = [
        "robe",
        "martin",
        "etc",
        "clay",
        "chauvet",
        "adj",
        "robert",
        "juliat",
        "source",
        "mac",
    ]


    def analyze(
        self,
        metadata: dict,
    ) -> dict:
        """
        Analyze Capture metadata.

        Returns detected project elements.
        """

        strings = []

        strings.extend(
            metadata.get(
                "ascii_strings",
                [],
            )
        )

        strings.extend(
            metadata.get(
                "utf16_strings",
                [],
            )
        )


        return {

            "fixtures": self._find_fixtures(
                strings
            ),

            "universes": self._find_universes(
                strings
            ),

            "scenes": self._find_scenes(
                strings
            ),

            "groups": self._find_groups(
                strings
            ),

        }



    def _find_fixtures(
        self,
        strings,
    ):

        fixtures = []


        for value in strings:

            lower = value.lower()


            if any(
                key in lower
                for key in self.FIXTURE_KEYWORDS
            ):

                fixtures.append(
                    {
                        "name": value
                    }
                )


        return fixtures



    def _find_universes(
        self,
        strings,
    ):

        result = []


        pattern = re.compile(
            r"universe\s*(\d+)",
            re.IGNORECASE,
        )


        for value in strings:

            match = pattern.search(
                value
            )


            if match:

                result.append(
                    {
                        "universe": int(
                            match.group(1)
                        )
                    }
                )


        return result



    def _find_scenes(
        self,
        strings,
    ):

        result = []


        for value in strings:

            if "scene" in value.lower():

                result.append(
                    {
                        "name": value
                    }
                )


        return result



    def _find_groups(
        self,
        strings,
    ):

        result = []


        for value in strings:

            if "group" in value.lower():

                result.append(
                    {
                        "name": value
                    }
                )


        return result