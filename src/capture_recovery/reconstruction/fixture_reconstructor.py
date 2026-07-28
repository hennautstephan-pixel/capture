"""
Fixture reconstruction.

Creates CaptureFixture objects
from semantic fixtures.
"""

from __future__ import annotations

from capture_recovery.formats import (
    CaptureFixture,
)

from .property_mapper import (
    PropertyMapper,
)


class FixtureReconstructor:
    """
    Reconstruct Capture fixtures.
    """

    def __init__(
        self,
        mapper=None,
    ) -> None:

        self.mapper = (
            mapper
            or PropertyMapper()
        )


    def can_reconstruct(
        self,
        obj,
    ) -> bool:

        return obj.object_type in (
            "Fixture",
            "Projector",
            "Light",
        )


    def reconstruct(
        self,
        obj,
    ) -> CaptureFixture:
        """
        Build CaptureFixture.
        """

        data = self.mapper.map(
            obj,
        )

        return CaptureFixture(

            name=str(
                obj.identifier,
            ),

            universe=data[
                "universe"
            ],

            address=data[
                "address"
            ],

            manufacturer=data[
                "manufacturer"
            ],

            model=data[
                "model"
            ],

            mode=data[
                "mode"
            ],

            properties=data,
        )