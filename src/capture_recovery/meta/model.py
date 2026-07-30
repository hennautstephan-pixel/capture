from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from capture_recovery.models.data_type import DataType


class Cardinality(Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    REPEATED = "repeated"


@dataclass(slots=True, frozen=True)
class FieldDefinition:
    """
    Describes a semantic field of a Capture object.
    """

    name: str
    datatype: DataType
    cardinality: Cardinality = Cardinality.OPTIONAL

    description: str = ""

    default: object = None

    confidence: float = 1.0

    aliases: tuple[str, ...] = ()

    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ObjectDefinition:
    """
    Describes an object that can be generated.
    """

    name: str

    description: str = ""

    fields: tuple[FieldDefinition, ...] = ()

    base_class: str = "SemanticObject"

    generate_signature: bool = True

    generate_builder: bool = True

    generate_decoder: bool = True

    generate_tests: bool = True

    metadata: dict[str, object] = field(default_factory=dict)