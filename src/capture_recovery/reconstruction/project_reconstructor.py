"""
Project reconstruction engine.

Converts semantic objects and relations
into a CaptureProject.
"""

from __future__ import annotations

from capture_recovery.formats import (
    CaptureProject,
    CaptureScene,
)

from capture_recovery.formats import (
    CaptureFixture,
)

from capture_recovery.formats import (
    SceneNode,
)

from .reconstruction_rules import (
    ReconstructionRules,
)


class ProjectReconstructor:
    """
    Rebuild Capture projects.
    """

    def __init__(
        self,
        rules=None,
    ) -> None:

        self.rules = (
            rules
            or ReconstructionRules()
        )


    def reconstruct(
        self,
        objects,
        relations=None,
        name="Recovered Project",
    ) -> CaptureProject:
        """
        Create a CaptureProject from
        semantic objects.
        """

        project = CaptureProject(
            name=name,
        )

        scene = CaptureScene()


        for obj in objects:

            if self.rules.is_fixture(
                obj,
            ):

                fixture = CaptureFixture(
                    name=str(
                        obj.identifier,
                    ),
                )

                project.add_fixture(
                    fixture,
                )


            node = SceneNode(
                name=str(
                    obj.identifier,
                ),

                parent=(
                    obj.properties.get(
                        "parent"
                    )
                ),

                properties=(
                    obj.properties.copy()
                ),
            )

            scene.add_node(
                node,
            )


        project.set_scene(
            scene,
        )

        return project