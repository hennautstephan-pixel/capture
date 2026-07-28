"""
Rotation mathematics.

Provides basic 3D rotation helpers.
"""

from __future__ import annotations

import math


class RotationMath:
    """
    Utility class for 3D rotations.
    """

    @staticmethod
    def degrees_to_radians(
        value: float,
    ) -> float:

        return math.radians(
            value,
        )

    @staticmethod
    def rotate_x(
        point: tuple[float, float, float],
        angle: float,
    ) -> tuple[float, float, float]:

        x, y, z = point

        rad = math.radians(
            angle,
        )

        cos_a = math.cos(
            rad,
        )

        sin_a = math.sin(
            rad,
        )

        return (
            x,

            y * cos_a - z * sin_a,

            y * sin_a + z * cos_a,
        )

    @staticmethod
    def rotate_y(
        point: tuple[float, float, float],
        angle: float,
    ) -> tuple[float, float, float]:

        x, y, z = point

        rad = math.radians(
            angle,
        )

        cos_a = math.cos(
            rad,
        )

        sin_a = math.sin(
            rad,
        )

        return (
            x * cos_a + z * sin_a,

            y,

            -x * sin_a + z * cos_a,
        )

    @staticmethod
    def rotate_z(
        point: tuple[float, float, float],
        angle: float,
    ) -> tuple[float, float, float]:

        x, y, z = point

        rad = math.radians(
            angle,
        )

        cos_a = math.cos(
            rad,
        )

        sin_a = math.sin(
            rad,
        )

        return (
            x * cos_a - y * sin_a,

            x * sin_a + y * cos_a,

            z,
        )

    @classmethod
    def rotate_xyz(
        cls,
        point: tuple[float, float, float],
        rotation: tuple[float, float, float],
    ) -> tuple[float, float, float]:

        result = point

        result = cls.rotate_x(
            result,
            rotation[0],
        )

        result = cls.rotate_y(
            result,
            rotation[1],
        )

        result = cls.rotate_z(
            result,
            rotation[2],
        )

        return result