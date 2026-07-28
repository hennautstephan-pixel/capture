"""
Public recovery API.

Provides a simple entry point
for Capture project recovery.
"""

from __future__ import annotations


from capture_recovery.pipeline import (
    FullRecoveryPipeline,
    ProjectRecoveryPipeline,
)



def recover(
    path,
    reconstructor=None,
) :
    """
    Recover a Capture project.

    Parameters
    ----------
    path:
        Capture project file path.

    reconstructor:
        Optional project reconstructor.

    Returns
    -------
    dict
        Recovery result.
    """


    full_pipeline = FullRecoveryPipeline()


    binary_result = full_pipeline.recover(
        path,
    )


    semantic_objects = (
        binary_result
        ["semantic"]
        ["objects"]
    )


    project_pipeline = ProjectRecoveryPipeline(
        reconstructor=reconstructor,
    )


    project_result = (
        project_pipeline.recover(
            semantic_objects,
        )
    )


    return {

        "project": project_result["project"],

        "validation": project_result["validation"],

        "binary": binary_result["binary"],

        "semantic": binary_result["semantic"],

    }