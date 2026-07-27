from __future__ import annotations

from capture_recovery.knowledge.decoder import Decoder
from capture_recovery.knowledge.fixture import Fixture
from capture_recovery.structures.field import Field
from capture_recovery.structures.structure import Structure


class FixtureDecoder(Decoder):
    """
    Decode reconstructed structures into Fixture objects.

    Recognition is heuristic-based. A confidence score is computed from the
    presence of characteristic fields.
    """

    MINIMUM_SCORE = 70

    FIELD_SCORES = {
        "name": 30,
        "universe": 20,
        "address": 20,
        "position": 20,
        "rotation": 10,
    }

    def can_decode(
        self,
        structure: Structure,
    ) -> bool:
        return self.score(structure) >= self.MINIMUM_SCORE

    def decode(
        self,
        structure: Structure,
    ) -> Fixture | None:

        if not self.can_decode(structure):
            return None

        return Fixture(
            object_type="Fixture",
            identifier=self._identifier(structure),
            confidence=self.score(structure) / 100.0,
            name=self._string(structure, "name") or "",
            universe=self._int(structure, "universe"),
            address=self._int(structure, "address"),
            position=self._tuple(structure, "position"),
            rotation=self._tuple(structure, "rotation"),
        )

    def score(
        self,
        structure: Structure,
    ) -> int:

        score = 0

        names = {
            field.name.lower()
            for field in structure.fields
        }

        for field_name, value in self.FIELD_SCORES.items():

            if field_name in names:
                score += value

        return score

    def _field(
        self,
        structure: Structure,
        name: str,
    ) -> Field | None:

        name = name.lower()

        for field in structure.fields:

            if field.name.lower() == name:
                return field

        return None

    def _string(
        self,
        structure: Structure,
        name: str,
    ) -> str | None:

        field = self._field(structure, name)

        if field is None:
            return None

        if field.value is None:
            return None

        return str(field.value)

    def _int(
        self,
        structure: Structure,
        name: str,
    ) -> int | None:

        field = self._field(structure, name)

        if field is None:
            return None

        try:
            return int(field.value)
        except (TypeError, ValueError):
            return None

    def _tuple(
        self,
        structure: Structure,
        name: str,
    ) -> tuple[float, float, float] | None:

        field = self._field(structure, name)

        if field is None:
            return None

        value = field.value

        if (
            isinstance(value, tuple)
            and len(value) == 3
        ):
            return (
                float(value[0]),
                float(value[1]),
                float(value[2]),
            )

        return None

    def _identifier(
        self,
        structure: Structure,
    ) -> str:

        name = self._string(structure, "name")

        if name:
            return name

        return f"fixture@{structure.offset}"