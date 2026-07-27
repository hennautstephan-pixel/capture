"""
Generator producing a Python decoder from an ObjectDefinition.
"""

from __future__ import annotations

from pathlib import Path

from capture_recovery.builders.decoder_method_builder import DecoderMethodBuilder
from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.python.python_class import PythonClass
from capture_recovery.python.python_import import PythonImport
from capture_recovery.python.python_module import PythonModule
from capture_recovery.writers.python_writer import PythonWriter

from .base import Generator
from .context import GenerationContext
from .generated_file import GeneratedFile


class DecoderGenerator(Generator):
    """
    Generate a decoder class for an ObjectDefinition.
    """

    @property
    def name(self) -> str:
        return "decoder"

    def generate(
        self,
        definition: ObjectDefinition,
        context: GenerationContext,
    ) -> tuple[GeneratedFile, ...]:

        module = PythonModule(
            name=f"{definition.name.lower()}_decoder",
        )

        module = module.add_import(
            PythonImport(
                module="capture_recovery.binary_reader",
                names=("BinaryReader",),
            )
        )

        module = module.add_import(
            PythonImport(
                module=definition.name.lower(),
                names=(definition.name,),
            )
        )

        cls = PythonClass(
            name=f"{definition.name}Decoder",
        )

        cls = cls.add_method(
            DecoderMethodBuilder().build(definition)
        )

        module = module.add_class(cls)

        source = PythonWriter().write(module)

        generated = GeneratedFile(
            path=context.resolve(
                Path(f"{definition.name.lower()}_decoder.py")
            ),
            content=source,
        )

        return (generated,)