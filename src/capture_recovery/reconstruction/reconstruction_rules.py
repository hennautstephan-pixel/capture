"""
Reconstruction rules.

Determine which semantic objects
can become Capture project elements.
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

        "FixtureCandidate",

        "fixture_object",

        "light",

    }



    def is_fixture(
        self,
        obj,
    ) -> bool:
        """
        Check if object can become
        a Capture fixture.

        Supports:
        - SemanticObject instances
        - dictionaries
        """



        object_type = self._get_value(
            obj,
            "object_type",
        )



        if object_type is None:

            object_type = self._get_value(
                obj,
                "type",
            )



        return (

            object_type

            in

            self.FIXTURE_TYPES

        )



    def _get_value(
        self,
        obj,
        key,
    ):
        """
        Read value from dict or object.
        """



        if isinstance(
            obj,
            dict,
        ):

            return obj.get(
                key,
            )



        return getattr(
            obj,
            key,
            None,
        )