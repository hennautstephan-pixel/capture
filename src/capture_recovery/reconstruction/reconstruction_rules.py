"""
Reconstruction rules.

Defines how semantic recovery objects
are converted into Capture objects.
"""

from __future__ import annotations





class ReconstructionRules:
    """
    Rules used during project reconstruction.
    """



    FIXTURE_TYPES = {

        "fixture",

        "Fixture",

        "fixture_candidate",

    }


    STRUCTURE_TYPES = {

        "structure",

        "scene_structure",

        "Structure",

    }


    GROUP_TYPES = {

        "group",

        "Group",

    }


    BINDING_TYPES = {

        "binding",

        "structure_binding",

        "Binding",

    }


    PROJECT_TYPES = {

        "project",

        "Project",

    }





    def __init__(
        self,
        min_confidence: float = 0.5,
    ) -> None:

        self.min_confidence = (
            min_confidence
        )





    def confidence_ok(
        self,
        obj,
    ) -> bool:
        """
        Check confidence threshold.
        """

        confidence = self._get(
            obj,
            "confidence",
            0.0,
        )


        return (
            confidence
            >=
            self.min_confidence
        )





    def is_project(
        self,
        obj,
    ) -> bool:
        """
        Check project object.
        """

        return (

            self._type(obj)

            in

            self.PROJECT_TYPES

        )





    def is_fixture(
        self,
        obj,
    ) -> bool:
        """
        Check if object can become
        a real Capture fixture.
        """

        object_type = self._type(
            obj,
        )


        #
        # Normalisation
        #

        normalized = object_type.lower()



        #
        # Legacy objects
        #
        # Existing reconstruction objects
        # are already trusted.
        #

        if normalized == "fixture":

            return True



        #
        # Reverse candidates
        #
        # Need additional proof.
        #

        if normalized != "fixture_candidate":

            return False



        confidence = self._get(
            obj,
            "confidence",
            0.0,
        )


        properties = self._properties(
            obj,
        )



        evidence = properties.get(
            "evidence",
            [],
        )


        manufacturer = properties.get(
            "manufacturer",
        )


        model = properties.get(
            "model",
        )


        address = properties.get(
            "address",
        )


        universe = properties.get(
            "universe",
        )



        #
        # Strong confidence
        #

        if confidence >= 0.80:

            return True



        #
        # Real Capture information
        #

        if manufacturer and model:

            return True



        if address is not None:

            return True



        if universe is not None:

            return True



        if len(evidence) >= 2:

            return True



        #
        # GUID alone is not enough
        #

        return False





    def is_fixture_candidate(
        self,
        obj,
    ) -> bool:
        """
        Keep weak candidates.
        """

        return (

            self._type(obj)

            .lower()

            ==

            "fixture_candidate"

        )





    def is_structure(
        self,
        obj,
    ) -> bool:

        return (

            self._type(obj)

            in

            self.STRUCTURE_TYPES

        )





    def is_group(
        self,
        obj,
    ) -> bool:

        return (

            self._type(obj)

            in

            self.GROUP_TYPES

        )





    def is_binding(
        self,
        obj,
    ) -> bool:

        return (

            self._type(obj)

            in

            self.BINDING_TYPES

        )





    def _type(
        self,
        obj,
    ) -> str:
        """
        Get object type from dict
        or SemanticObject.
        """

        if isinstance(
            obj,
            dict,
        ):

            return obj.get(
                "object_type",
                "",
            )



        return getattr(
            obj,
            "object_type",
            "",
        )





    def _get(
        self,
        obj,
        key,
        default=None,
    ):

        if isinstance(
            obj,
            dict,
        ):

            return obj.get(
                key,
                default,
            )



        return getattr(
            obj,
            key,
            default,
        )





    def _properties(
        self,
        obj,
    ) -> dict:
        """
        Extract properties.
        """

        if isinstance(
            obj,
            dict,
        ):

            return obj.get(
                "properties",
                {},
            )



        return getattr(
            obj,
            "properties",
            {},
        )