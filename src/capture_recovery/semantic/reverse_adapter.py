"""
capture_recovery.semantic.reverse_adapter

Convert reverse analysis results into
semantic recovery objects.

Version v10:
- dense GUID scan suppression
- sliding window filtering
- balanced fixture candidate recovery
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
    Transform reverse analysis results
    into semantic recovery objects.
    """



    def __init__(
        self,
        min_confidence: float = 0.5,
    ) -> None:

        self.min_confidence = min_confidence





    def analyze(
        self,
        reverse_result,
    ) -> dict:


        objects = self.adapt(
            reverse_result
        )


        return {

            "objects":
                [
                    obj.as_dict()
                    for obj in objects
                ],

            "evidence":
                {

                    "strings":
                        self._serialize(
                            getattr(
                                reverse_result,
                                "strings",
                                (),
                            )
                        ),

                    "guids":
                        self._serialize(
                            getattr(
                                reverse_result,
                                "guids",
                                (),
                            )
                        ),

                    "numeric":
                        self._serialize(
                            getattr(
                                reverse_result,
                                "numeric",
                                (),
                            )
                        ),

                },

        }





    def adapt(
        self,
        reverse_result,
    ) -> list[SemanticObject]:


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



        for guid in self._cluster_guids(
            guids
        ):


            evidence = self._find_near_strings(
                guid,
                strings,
            )


            confidence = 0.35


            if evidence:

                confidence = 0.65



            objects.append(

                SemanticObject(

                    identifier=
                        f"Fixture_{guid.offset}",


                    object_type=
                        "fixture_candidate",


                    confidence=
                        confidence,


                    properties={

                        "guid":
                            guid.value,

                        "offset":
                            guid.offset,

                        "source":
                            "binary_guid",

                        "evidence":
                            evidence,

                    },

                )

            )



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





    def _cluster_guids(
        self,
        guids,
    ):
        """
        Remove dense GUID scans.

        Example:

        128
        130
        132
        134

        becomes:

        128
        """

        if not guids:

            return []



        ordered = sorted(

            guids,

            key=lambda item:

                getattr(
                    item,
                    "offset",
                    0,
                )

        )


        result = []


        i = 0


        total = len(
            ordered
        )



        while i < total:


            current = ordered[i]


            if self._guid_score(
                current
            ) <= 0:

                i += 1

                continue



            start = getattr(
                current,
                "offset",
                0,
            )


            cluster = [

                current

            ]



            j = i + 1



            while j < total:


                offset = getattr(
                    ordered[j],
                    "offset",
                    0,
                )


                if offset - start <= 32:

                    cluster.append(
                        ordered[j]
                    )

                    j += 1

                else:

                    break



            #
            # Dense binary area
            #

            if len(cluster) >= 4:


                best = max(

                    cluster,

                    key=self._guid_score,

                )


                result.append(
                    best
                )


                i = j



            else:


                result.append(
                    current
                )


                i += 1



        return result





    def _guid_score(
        self,
        guid,
    ) -> float:


        raw = getattr(
            guid,
            "raw_bytes",
            b"",
        )


        if len(raw) != 16:

            return 0.0



        if raw.count(
            0
        ) == 16:

            return 0.0



        printable = sum(

            1

            for byte in raw

            if 32 <= byte <= 126

        )


        if printable == 16:

            return 0.0



        return 1.0





    def _find_near_strings(
        self,
        guid,
        strings,
    ) -> list:


        result = []


        offset = getattr(
            guid,
            "offset",
            0,
        )


        for item in strings:


            item_offset = getattr(
                item,
                "offset",
                -999,
            )


            if abs(
                item_offset - offset
            ) <= 128:


                value = getattr(
                    item,
                    "value",
                    "",
                )


                if value:

                    result.append(
                        value
                    )


        return result





    def _extract_metadata(
        self,
        strings,
    ) -> dict:


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





    def _serialize(
        self,
        values,
    ) -> list:


        result = []


        for item in values:


            if hasattr(
                item,
                "as_dict",
            ):

                result.append(
                    item.as_dict()
                )

            else:

                result.append(
                    str(item)
                )


        return result