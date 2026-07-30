"""
Project reconstruction.

Transforms semantic recovery objects
into Capture project models.
"""

from __future__ import annotations


from capture_recovery.formats.capture_project import (
    CaptureProject,
    CaptureFixture,
)


from capture_recovery.reconstruction.reconstruction_rules import (
    ReconstructionRules,
)





class ProjectReconstructor:
    """
    Build a CaptureProject from
    semantic recovery objects.
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
    ) -> CaptureProject:
        """
        Reconstruct Capture project.
        """

        project = CaptureProject(
            name="Recovered Project"
        )


        candidates = []


        for obj in objects:


            if self.rules.is_project(
                obj
            ):

                project.metadata.update(
                    self._properties(obj)
                )



            elif self.rules.is_fixture(
                obj
            ):

                fixture = self._build_fixture(
                    obj
                )


                project.add_fixture(
                    fixture
                )


                self._add_scene_node(
                    project,
                    fixture,
                    obj,
                )



            elif self.rules.is_fixture_candidate(
                obj
            ):

                candidates.append(
                    self._serialize_candidate(obj)
                )



            elif self.rules.is_structure(
                obj
            ):

                project.metadata.setdefault(
                    "structures",
                    [],
                ).append(
                    self._properties(obj)
                )



            elif self.rules.is_group(
                obj
            ):

                project.metadata.setdefault(
                    "groups",
                    [],
                ).append(
                    self._properties(obj)
                )



        if candidates:

            project.metadata[
                "fixture_candidates"
            ] = candidates



        project.metadata.update(
            {

                "recovered": True,

                "source":
                    "reverse_analysis",

                "objects":
                    len(objects),

                "fixtures":
                    len(project.fixtures),

                "candidates":
                    len(candidates),

            }
        )


        return project





    def _build_fixture(
        self,
        obj,
    ) -> CaptureFixture:
        """
        Create Capture fixture.
        """

        properties = self._properties(
            obj
        )


        return CaptureFixture(

            name=self._get(
                obj,
                "identifier",
                "Recovered Fixture",
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


            properties=properties,

        )





    def _add_scene_node(
        self,
        project,
        fixture,
        source,
    ) -> None:
        """
        Add fixture to existing Capture scene.
        """

        scene = project.scene


        name = fixture.name


        if name in scene.nodes:

            return



        properties = self._properties(
            source
        )


        parent = properties.get(
            "parent"
        )



        #
        # Existing scene model
        # does not expose CaptureSceneNode.
        #

        node = type(
            "SceneNode",
            (),
            {

                "name":
                    name,


                "parent":
                    parent,


                "children":
                    [],


                "properties":
                    {

                        "type":
                            "fixture",


                        "recovered":
                            True,

                    },

            },
        )()



        scene.nodes[name] = node



        if parent is None:

            if name not in scene.root_nodes:

                scene.root_nodes.append(
                    name
                )





    def _serialize_candidate(
        self,
        obj,
    ) -> dict:

        return {

            "identifier":
                self._get(
                    obj,
                    "identifier",
                    "",
                ),


            "confidence":
                self._get(
                    obj,
                    "confidence",
                    0.0,
                ),


            "properties":
                self._properties(
                    obj
                ),

        }





    def _properties(
        self,
        obj,
    ) -> dict:


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