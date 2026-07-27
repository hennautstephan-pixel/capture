from __future__ import annotations

from dataclasses import dataclass, field

from .field_signature import FieldSignature


@dataclass(slots=True, frozen=True)
class Signature:
    """
    Describes the expected structure of a semantic object.

    A Signature is composed of required and optional field signatures.
    It is used by the SignatureEngine to recognize reconstructed
    binary structures.
    """

    name: str

    required: tuple[FieldSignature, ...] = field(default_factory=tuple)

    optional: tuple[FieldSignature, ...] = field(default_factory=tuple)

    minimum_score: int = 70

    description: str = ""

    @property
    def fields(self) -> tuple[FieldSignature, ...]:
        """
        Return every field signature.
        """
        return self.required + self.optional

    @property
    def maximum_score(self) -> int:
        """
        Maximum score obtainable with this signature.
        """
        return sum(field.weight for field in self.fields)

    def required_names(self) -> tuple[str, ...]:
        """
        Return required field names.
        """
        return tuple(field.name for field in self.required)

    def optional_names(self) -> tuple[str, ...]:
        """
        Return optional field names.
        """
        return tuple(field.name for field in self.optional)

    def field(
        self,
        name: str,
    ) -> FieldSignature | None:
        """
        Find a field signature by name.
        """

        name = name.lower()

        for field in self.fields:
            if field.name.lower() == name:
                return field

        return None

    def contains(
        self,
        name: str,
    ) -> bool:
        """
        Return True if the signature contains a field.
        """
        return self.field(name) is not None

    def __len__(self) -> int:
        return len(self.fields)

    def __iter__(self):
        return iter(self.fields)

    def __contains__(self, name: str) -> bool:
        return self.contains(name)

    def __str__(self) -> str:
        return (
            f"{self.name}"
            f"(required={len(self.required)}, "
            f"optional={len(self.optional)}, "
            f"score={self.maximum_score})"
        )