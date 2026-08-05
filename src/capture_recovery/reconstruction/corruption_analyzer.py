from __future__ import annotations

from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class CorruptionRegion:
    """
    Represents a corrupted byte range.
    """

    offset: int

    size: int



@dataclass(frozen=True, slots=True)
class CorruptionAnalysis:
    """
    Result of corruption analysis.
    """

    total_size: int

    corrupted_bytes: int

    regions: tuple[CorruptionRegion, ...]



    @property
    def corruption_ratio(
        self,
    ) -> float:
        """
        Percentage of corrupted data.
        """

        if self.total_size == 0:

            return 0.0


        return (
            self.corrupted_bytes /
            self.total_size
        )



class CorruptionAnalyzer:
    """
    Compare a damaged binary stream
    against a reference stream.
    """



    def analyze(
        self,
        corrupted: bytes,
        reference: bytes,
    ) -> CorruptionAnalysis:
        """
        Detect corrupted regions.
        """

        size = max(
            len(corrupted),
            len(reference),
        )


        regions = []

        corrupted_count = 0


        current_start = None


        for index in range(size):

            left = (
                corrupted[index]
                if index < len(corrupted)
                else None
            )


            right = (
                reference[index]
                if index < len(reference)
                else None
            )


            different = (
                left != right
            )


            if different:

                corrupted_count += 1


                if current_start is None:

                    current_start = index


            else:

                if current_start is not None:

                    regions.append(
                        CorruptionRegion(
                            offset=current_start,

                            size=index - current_start,
                        )
                    )

                    current_start = None



        if current_start is not None:

            regions.append(
                CorruptionRegion(
                    offset=current_start,

                    size=size - current_start,
                )
            )


        return CorruptionAnalysis(
            total_size=size,

            corrupted_bytes=corrupted_count,

            regions=tuple(
                regions
            ),
        )