"""
capture_recovery.reverse.reverse_engine

Main reverse analysis orchestration engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .alignment_detector import AlignmentDetector
from .alignment_value import AlignmentValue
from .detection_options import DetectionOptions
from .entropy_detector import EntropyDetector
from .entropy_value import EntropyValue
from .guid_detector import GuidDetector
from .guid_value import GuidValue
from .numeric_detector import NumericDetector
from .numeric_value import NumericValue
from .registry import ReverseRegistry
from .string_detector import StringDetector
from .string_value import StringValue



@dataclass(
    frozen=True,
    slots=True,
)
class ReverseResult:
    """
    Complete reverse analysis result.
    """

    numeric: tuple[NumericValue, ...] = field(
        default_factory=tuple
    )

    strings: tuple[StringValue, ...] = field(
        default_factory=tuple
    )

    guids: tuple[GuidValue, ...] = field(
        default_factory=tuple
    )

    alignments: tuple[AlignmentValue, ...] = field(
        default_factory=tuple
    )

    entropy: tuple[EntropyValue, ...] = field(
        default_factory=tuple
    )


    @property
    def total(self) -> int:

        return (
            len(self.numeric)
            +
            len(self.strings)
            +
            len(self.guids)
            +
            len(self.alignments)
            +
            len(self.entropy)
        )



class ReverseEngine:
    """
    Execute reverse detectors through registry.
    """


    def __init__(
        self,
        registry: ReverseRegistry | None = None,
    ) -> None:


        if registry is not None:

            self.registry = registry

        else:

            self.registry = (
                self._create_default_registry()
            )



    @staticmethod
    def _create_default_registry() -> ReverseRegistry:
        """
        Create default detector registry.
        """

        return ReverseRegistry(
            (
                NumericDetector(),
                StringDetector(),
                GuidDetector(),
                AlignmentDetector(),
                EntropyDetector(),
            )
        )



    def analyze(
        self,
        data: bytes,
        options: DetectionOptions | None = None,
    ) -> ReverseResult:
        """
        Analyze binary data.
        """


        if options is None:

            # Protection uniquement pour les gros fichiers
            if len(data) > 1024 * 1024:

                options = DetectionOptions(
                    max_results=500,
                    max_scan_size=1024 * 1024,
                )

            else:

                options = DetectionOptions()



        # Respecter un registre personnalisé vide
        detectors = tuple(
            self.registry.all()
        )

        if not detectors:

            return ReverseResult()



        numeric = ()

        strings = ()

        guids = ()

        alignments = ()

        entropy = ()



        for detector in detectors:


            print(
                f"[Reverse] START "
                f"{detector.__class__.__name__}",
                flush=True,
            )


            results = detector.detect(
                data,
                options,
            )


            print(
                f"[Reverse] END "
                f"{detector.__class__.__name__} : "
                f"{len(results)}",
                flush=True,
            )



            if isinstance(
                detector,
                NumericDetector,
            ):

                numeric = tuple(results)



            elif isinstance(
                detector,
                StringDetector,
            ):

                strings = tuple(results)



            elif isinstance(
                detector,
                GuidDetector,
            ):

                guids = tuple(results)



            elif isinstance(
                detector,
                AlignmentDetector,
            ):

                alignments = tuple(results)



            elif isinstance(
                detector,
                EntropyDetector,
            ):

                entropy = tuple(results)



        return ReverseResult(

            numeric=numeric,

            strings=strings,

            guids=guids,

            alignments=alignments,

            entropy=entropy,

        )