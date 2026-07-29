"""
Project reconstruction engine.

Converts semantic objects into
CaptureProject models.
"""

from __future__ import annotations


from capture_recovery.formats import (
    CaptureProject,
    CaptureScene,
    CaptureFixture,
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
        Convert semantic objects
        into CaptureProject.
        """



        project = CaptureProject(
            name=name,
        )


        scene = CaptureScene()



        fixture_number = 1



        for obj in objects:


            #
            # Normalize dict/object format
            #

            semantic = self._normalize_object(
                obj
            )



            if self.rules.is_fixture(
                semantic,
            ):


                fixture = self._build_fixture(
                    semantic,
                    fixture_number,
                )


                fixture_number += 1



                project.add_fixture(
                    fixture,
                )



            node = SceneNode(

                name=str(
                    semantic["identifier"]
                ),


                parent=(

                    semantic["properties"].get(
                        "parent"
                    )

                ),


                properties={

                    "object_type":

                        semantic["object_type"],


                    "confidence":

                        semantic["confidence"],


                    **semantic["properties"],

                },

            )


            scene.add_node(
                node,
            )



        project.metadata.update(

            {

                "recovered":

                    True,


                "source":

                    "reverse_analysis",


                "objects":

                    len(objects),

            }

        )



        project.set_scene(
            scene,
        )



        return project



    def _normalize_object(
        self,
        obj,
    ) -> dict:
        """
        Convert SemanticObject or dict
        into common dictionary format.
        """



        if isinstance(
            obj,
            dict,
        ):

            return {

                "identifier":

                    obj.get(
                        "identifier",
                        "unknown",
                    ),


                "object_type":

                    obj.get(
                        "object_type",
                        obj.get(
                            "type",
                            "unknown",
                        ),
                    ),


                "confidence":

                    obj.get(
                        "confidence",
                        0.0,
                    ),


                "properties":

                    obj.get(
                        "properties",
                        {},
                    ),

            }



        return {

            "identifier":

                getattr(
                    obj,
                    "identifier",
                    "unknown",
                ),


            "object_type":

                getattr(
                    obj,
                    "object_type",
                    "unknown",
                ),


            "confidence":

                getattr(
                    obj,
                    "confidence",
                    0.0,
                ),


            "properties":

                getattr(
                    obj,
                    "properties",
                    {},
                ),

        }



    def _build_fixture(
        self,
        obj,
        number,
    ) -> CaptureFixture:
        """
        Build CaptureFixture.
        """



        return CaptureFixture(

            name=(

                f"Recovered Fixture {number:03d}"

            ),


            universe=0,


            address=0,


            manufacturer=None,


            model=None,


            mode=None,


            properties={

                "recovered":

                    True,


                "confidence":

                    obj["confidence"],


                "source":

                    obj["object_type"],


                **obj["properties"],

            },

        )