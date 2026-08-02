"""
capture_recovery.semantic.reverse_structure_adapter

Convert ReverseResult into DetectionIndex.
"""

from __future__ import annotations

from capture_recovery.indexes import DetectionIndex

from capture_recovery.models import (
    DataType,
    Detection,
)

from capture_recovery.reverse.reverse_engine import (
    ReverseResult,
)

from capture_recovery.reverse.numeric_value import (
    NumericValue,
)

from capture_recovery.reverse.string_value import (
    StringValue,
)

from capture_recovery.reverse.guid_value import (
    GuidValue,
)

from capture_recovery.reverse.alignment_value import (
    AlignmentValue,
)

from capture_recovery.reverse.entropy_value import (
    EntropyValue,
)


class ReverseStructureAdapter:
    """
    Convert ReverseResult into DetectionIndex.

    This adapter is intentionally simple.

    ReverseResult
            │
            ▼
    DetectionIndex
    """

    def adapt(
        self,
        reverse: ReverseResult,
    ) -> DetectionIndex:

        detections: list[Detection] = []

        detections.extend(
            self._convert_numeric(
                reverse.numeric,
            )
        )

        detections.extend(
            self._convert_strings(
                reverse.strings,
            )
        )

        detections.extend(
            self._convert_guids(
                reverse.guids,
            )
        )

        detections.extend(
            self._convert_alignments(
                reverse.alignments,
            )
        )

        detections.extend(
            self._convert_entropy(
                reverse.entropy,
            )
        )

        return self._build_index(
            detections,
        )

    def __call__(
        self,
        reverse: ReverseResult,
    ) -> DetectionIndex:

        return self.adapt(
            reverse,
        )

    # ==========================================================
    # Numeric
    # ==========================================================

    def _convert_numeric(
        self,
        values: tuple[NumericValue, ...],
    ) -> list[Detection]:

        return [
            self._numeric_detection(v)
            for v in values
        ]

    def _numeric_detection(
        self,
        value: NumericValue,
    ) -> Detection:

        return Detection(
            offset=value.offset,
            length=value.size,
            datatype=self._numeric_datatype(
                value.type_name,
            ),
            value=value.value,
            confidence=1.0,
            detector="NumericDetector",
            metadata={
                "numeric_type": value.type_name,
                "endianness": value.endianness,
            },
        )

    @staticmethod
    def _numeric_datatype(
        type_name: str,
    ) -> DataType:

        mapping = {
            "int8": DataType.INT8,
            "uint8": DataType.UINT8,
            "int16": DataType.INT16,
            "uint16": DataType.UINT16,
            "int32": DataType.INT32,
            "uint32": DataType.UINT32,
            "int64": DataType.INT64,
            "uint64": DataType.UINT64,
            "float32": DataType.FLOAT32,
            "float64": DataType.FLOAT64,
        }

        return mapping.get(
            type_name.lower(),
            DataType.UNKNOWN,
        )

        # ==========================================================
    # Strings
    # ==========================================================

    def _convert_strings(
        self,
        values: tuple[StringValue, ...],
    ) -> list[Detection]:

        return [
            self._string_detection(v)
            for v in values
        ]

    def _string_detection(
        self,
        value: StringValue,
    ) -> Detection:

        return Detection(
            offset=value.offset,
            length=value.length,
            datatype=self._string_datatype(
                value.type_name,
            ),
            value=value.value,
            confidence=1.0,
            detector="StringDetector",
            metadata={
                "encoding": value.encoding,
                "terminated": value.terminated,
                "raw_length": len(value.raw_bytes),
            },
        )

    @staticmethod
    def _string_datatype(
        type_name: str,
    ) -> DataType:

        mapping = {
            "ascii": DataType.ASCII,
            "utf8": DataType.UTF8,
            "utf16": DataType.UTF16,
            "utf16_le": DataType.UTF16,
            "utf16_be": DataType.UTF16,
            "utf16-le": DataType.UTF16,
            "utf16-be": DataType.UTF16,
        }

        return mapping.get(
            type_name.lower(),
            DataType.STRING,
        )

    # ==========================================================
    # GUID
    # ==========================================================

    def _convert_guids(
        self,
        values: tuple[GuidValue, ...],
    ) -> list[Detection]:

        return [
            self._guid_detection(v)
            for v in values
        ]

    def _guid_detection(
        self,
        value: GuidValue,
    ) -> Detection:

        return Detection(
            offset=value.offset,
            length=value.length,
            datatype=DataType.UUID,
            value=value.value,
            confidence=1.0,
            detector="GuidDetector",
            metadata={
                "guid_type": value.type_name,
                "windows_layout": value.is_windows,
            },
        )

    # ==========================================================
    # Alignment
    # ==========================================================

    def _convert_alignments(
        self,
        values: tuple[AlignmentValue, ...],
    ) -> list[Detection]:

        return [
            self._alignment_detection(v)
            for v in values
        ]

    def _alignment_detection(
        self,
        value: AlignmentValue,
    ) -> Detection:

        return Detection(
            offset=value.offset,
            length=value.length,
            datatype=DataType.STRUCT,
            value=value.alignment,
            confidence=value.score,
            detector="AlignmentDetector",
            metadata={
                "alignment": value.alignment,
                "aligned": value.is_aligned,
            },
        )

        # ==========================================================
    # Entropy
    # ==========================================================

    def _convert_entropy(
        self,
        values: tuple[EntropyValue, ...],
    ) -> list[Detection]:

        return [
            self._entropy_detection(v)
            for v in values
        ]

    def _entropy_detection(
        self,
        value: EntropyValue,
    ) -> Detection:

        return Detection(
            offset=value.offset,
            length=value.length,
            datatype=DataType.BYTES,
            value=value.entropy,
            confidence=value.score,
            detector="EntropyDetector",
            metadata={
                "entropy": value.entropy,
                "high_entropy": value.is_high_entropy,
            },
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _build_index(
        detections: list[Detection],
    ) -> DetectionIndex:
        """
        Build a DetectionIndex from detections.

        The DetectionIndex constructor expects detections
        to be sorted by offset.
        """

        detections.sort(
            key=lambda detection: (
                detection.offset,
                detection.length,
            ),
        )

        return DetectionIndex(
            detections,
        )