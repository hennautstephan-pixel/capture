from dataclasses import dataclass


@dataclass(slots=True)
class DecodeCoverage:

    total_objects: int = 0

    decoded_objects: int = 0

    unknown_objects: int = 0

    decoded_bytes: int = 0

    total_bytes: int = 0

    @property
    def object_ratio(self) -> float:

        if self.total_objects == 0:

            return 0.0

        return self.decoded_objects / self.total_objects

    @property
    def byte_ratio(self) -> float:

        if self.total_bytes == 0:

            return 0.0

        return self.decoded_bytes / self.total_bytes