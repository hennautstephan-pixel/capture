"""
capture_recovery.semantic.reverse_adapter

Convert reverse analysis results into
semantic recovery objects.
"""

from __future__ import annotations


from dataclasses import dataclass, field



@dataclass(slots=True)
class SemanticObject:
    """
    Recovered semantic object.
    """

    identifier: str

    object_type: str

    confidence: float = 0.0

    properties: dict = field(
        default_factory=dict
    )


    def as_dict(self) -> dict:
        """
        Convert object to JSON data.
        """

        return {

            "identifier":
                self.identifier,

            "object_type":
                self.object_type,

            "confidence":
                self.confidence,

            "properties":
                self.properties,

        }



class ReverseSemanticAdapter:
    """
    Transform ReverseResult into
    semantic recovery objects.
    """



    def __init__(
        self,
        min_confidence: float = 0.5,
    ) -> None:

        self.min_confidence = (
            min_confidence
        )



    def analyze(
        self,
        reverse_result,
    ) -> dict:
        """
        Compatibility API.

        Called by SemanticRecoveryPipeline.
        """

        objects = self.adapt(
            reverse_result,
        )


        strings = [

            item.as_dict()

            for item in getattr(
                reverse_result,
                "strings",
                (),
            )

            if hasattr(
                item,
                "as_dict",
            )

        ]


        guids = [

            item.as_dict()

            for item in getattr(
                reverse_result,
                "guids",
                (),
            )

            if hasattr(
                item,
                "as_dict",
            )

        ]


        numeric = [

            item.as_dict()

            for item in getattr(
                reverse_result,
                "numeric",
                (),
            )

            if hasattr(
                item,
                "as_dict",
            )

        ]



        return {

            "objects": [

                obj.as_dict()

                for obj in objects

            ],


            "evidence": {

                "strings":
                    strings,

                "guids":
                    guids,

                "numeric":
                    numeric,

            },

        }



    def adapt(
        self,
        reverse_result,
    ) -> list[SemanticObject]:
        """
        Convert reverse detections
        into semantic objects.
        """

        objects = []



        strings = getattr(
            reverse_result,
            "strings",
            (),
        )


        guids = getattr(
            reverse_result,
            "guids",
            (),
        )


        numerics = getattr(
            reverse_result,
            "numeric",
            (),
        )



        #
        # Capture project metadata
        #

        metadata = self._extract_metadata(
            strings
        )


        if metadata:

            objects.append(

                SemanticObject(

                    identifier="project",

                    object_type="project",

                    confidence=0.85,

                    properties=metadata,

                )

            )



        #
        # GUID recovery
        #
        # A GUID alone is not enough
        # to prove a fixture.
        #
        # It becomes a probable fixture
        # candidate.
        #

        for guid in guids:


            confidence = (
                self._guid_confidence(
                    guid
                )
            )


            if confidence < self.min_confidence:

                continue



            objects.append(

                SemanticObject(

                    identifier=(

                        f"Fixture_{guid.offset}"

                    ),


                    object_type="fixture_candidate",


                    confidence=0.65,


                    properties={

                        "guid":

                            guid.value,


                        "offset":

                            guid.offset,


                        "source":

                            "binary_guid",


                        "recovery":

                            "probable",

                    },

                )

            )



        #
        # Numeric evidence
        #

        if numerics:

            objects.append(

                SemanticObject(

                    identifier="numeric_data",

                    object_type="numeric_block",

                    confidence=0.55,

                    properties={

                        "count":

                            len(numerics),

                    },

                )

            )



        return objects



    def _extract_metadata(
        self,
        strings,
    ) -> dict:
        """
        Extract Capture metadata markers.
        """

        result = {}



        for item in strings:

            value = getattr(
                item,
                "value",
                "",
            )


            if value == "Project":

                result[

                    "has_project_marker"

                ] = True



            elif value == "SoftwareVersion":

                result[

                    "has_version_marker"

                ] = True



        return result



    @staticmethod
    def _guid_confidence(
        guid,
    ) -> float:
        """
        Estimate GUID reliability.
        """

        raw = getattr(
            guid,
            "raw_bytes",
            b"",
        )


        if len(raw) != 16:

            return 0.0



        zero_ratio = (

            raw.count(0)

            /

            16

        )



        if zero_ratio > 0.5:

            return 0.2



        return 0.75