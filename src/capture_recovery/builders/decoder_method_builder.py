"""
Builder creating a decode() method for generated decoders.
"""

from __future__ import annotations

from capture_recovery.builders.reader_type_mapper import ReaderTypeMapper
from capture_recovery.definitions.object_definition import ObjectDefinition
from capture_recovery.python.python_method import PythonMethod


class DecoderMethodBuilder:
    """
    Build the decode() method for a generated decoder.
    """

    def build(
        self,
        definition: ObjectDefinition,
    ) -> PythonMethod:

        mapper = ReaderTypeMapper()

        method = (
            PythonMethod(
                name="decode",
                return_type=definition.name,
            )
            .add_decorator("staticmethod")
            .add_parameter("reader: BinaryReader")
        )

        method = method.add_line(f"return {definition.name}(")

        for field in definition.fields:

            reader_call = mapper.method_for(field.python_type)

            method = method.add_line(
                f"    {field.name}=reader.{reader_call},"
            )

        method = method.add_line(")")

        return method