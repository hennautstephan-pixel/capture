"""
Capture fixture builder.

Builds Capture fixtures from recovered
semantic fixture objects.
"""

from __future__ import annotations

from capture_recovery.knowledge.semantic_object import (
    SemanticObject,
)

from .capture_project import (
    CaptureFixture,
)

from .fixture_geometry_builder import (
    FixtureGeometryBuilder,
)

from .position_builder import (
    PositionBuilder,
)

from .focus_builder import (
    FocusBuilder,
)

from .mount_builder import (
    MountBuilder,
)


class CaptureFixtureBuilder:
    """
    Build Capture fixtures.
    """

    def __init__(
        self,
        resolver=None,
        geometry_builder: FixtureGeometryBuilder | None = None,
        position_builder: PositionBuilder | None = None,
        focus_builder: FocusBuilder | None = None,
        mount_builder: MountBuilder | None = None,
    ) -> None:

        self.resolver = resolver

        self.geometry_builder = (
            geometry_builder
            or FixtureGeometryBuilder()
        )

        self.position_builder = (
            position_builder
            or PositionBuilder()
        )

        self.focus_builder = (
            focus_builder
            or FocusBuilder()
        )

        self.mount_builder = (
            mount_builder
            or MountBuilder()
        )

    def _resolve_library_data(
        self,
        fixture: SemanticObject,
    ) -> dict:

        if self.resolver is None:
            return {}

        resolved = self.resolver.resolve(
            fixture,
        )

        if resolved is None:
            return {}

        if isinstance(
            resolved,
            dict,
        ):
            return resolved.copy()

        data = {}

        for attribute in (
            "channels",
            "geometry",
            "placement",
            "manufacturer",
            "model",
            "mode",
        ):

            if hasattr(
                resolved,
                attribute,
            ):

                value = getattr(
                    resolved,
                    attribute,
                )

                if value is not None:
                    data[attribute] = value

        return data

    def build(
        self,
        fixture: SemanticObject,
    ) -> CaptureFixture:
        """
        Convert semantic fixture into
        Capture fixture.
        """

        source_properties = (
            fixture.properties.copy()
        )

        library_data = (
            self._resolve_library_data(
                fixture,
            )
        )

        properties = {
            **library_data,
            **source_properties,
        }

        geometry = (
            self.geometry_builder.build(
                fixture,
            )
        )

        geometry_data = {}

        if isinstance(
            properties.get(
                "geometry",
            ),
            dict,
        ):

            geometry_data.update(
                properties["geometry"],
            )

        if hasattr(
            geometry,
            "beam_angle",
        ):

            geometry_data.update(
                {
                    "beam_angle": geometry.beam_angle,
                    "field_angle": geometry.field_angle,
                    "zoom": geometry.zoom,
                }
            )

        position = (
            self.position_builder.build(
                fixture,
            )
        )

        focus_point = (
            self.focus_builder.build(
                fixture,
            )
        )

        mount = (
            self.mount_builder.build(
                fixture,
            )
        )

        placement = {
            "position": source_properties.get(
                "position",
            ),

            "rotation": source_properties.get(
                "rotation",
            ),

            "height": properties.get(
                "height",
                0.0,
            ),

            "focus_point": properties.get(
                "focus_point",
            ),

            "mount": properties.get(
                "mount",
            ),
        }

        final_properties = {
            **properties,

            "geometry": geometry_data,

            "placement": placement,
        }

        return CaptureFixture(
            name=str(
                fixture.identifier,
            ),

            universe=properties.get(
                "universe",
                0,
            ),

            address=properties.get(
                "address",
                0,
            ),

            manufacturer=properties.get(
                "manufacturer",
            ),

            model=properties.get(
                "model",
            ),

            mode=properties.get(
                "mode",
            ),

            position=position,

            focus_point=focus_point,

            mount=mount,

            properties=final_properties,
        )

    def can_build(
        self,
        fixture: SemanticObject,
    ) -> bool:

        return (
            fixture.object_type
            == "Fixture"
        )