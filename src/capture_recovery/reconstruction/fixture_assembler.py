"""
Fixture assembler.

Combines fixture data, transforms
and focus information.
"""

from __future__ import annotations

from capture_recovery.formats import (
    CaptureFixture,
)


class FixtureAssembler:
    """
    Assemble complete fixtures.
    """

    def assemble(
        self,
        fixture: CaptureFixture,
        transform=None,
        focus=None,
        mount=None,
    ) -> CaptureFixture:
        """
        Merge additional fixture data.
        """

        properties = fixture.properties.copy()


        if transform:

            properties.update(
                transform,
            )


        if focus:

            properties.update(
                focus,
            )


        if mount:

            properties["mount"] = (
                mount
            )


        fixture.properties = properties


        return fixture