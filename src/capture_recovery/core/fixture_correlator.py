from __future__ import annotations

from typing import Iterable

from capture_recovery.core.property_extractors import FixturePropertyExtractor
from capture_recovery.core.semantic_correlator import SemanticCorrelator, SemanticObject
from capture_recovery.core.value_clusterer import ValueCluster


class FixtureCorrelator(SemanticCorrelator):
    """A first specialized semantic correlator for fixture reconstruction.

    The current implementation recognizes a basic fixture pattern: a cluster with
    exactly one UUID and at least one string is treated as a fixture candidate.
    Other clusters remain as generic unknown semantic objects.
    """

    def __init__(self) -> None:
        """Initialize the correlator with a property extractor."""
        self._extractor = FixturePropertyExtractor()

    def _build_unknown(self, cluster: ValueCluster) -> SemanticObject:
        """Build the semantic object produced for an unknown cluster."""
        return SemanticObject(
            object_type="unknown",
            properties={"values": tuple(cluster.values)},
            confidence=1.0,
            source_offsets=tuple(value.offset for value in cluster.values),
        )

    def _build_fixture(
        self,
        cluster: ValueCluster,
        properties: object,
    ) -> SemanticObject:
        """Build the semantic object produced for a fixture-like cluster."""
        extracted = self._extractor.extract(cluster)
        payload: dict[str, object] = {
            "uuid": extracted.uuid,
            "name": extracted.name,
            "values": tuple(cluster.values),
        }

        if extracted.dmx_universe is not None:
            payload["dmx"] = {"universe": extracted.dmx_universe}
        if extracted.dmx_address is not None:
            dmx_payload = payload.get("dmx")
            if isinstance(dmx_payload, dict):
                dmx_payload["address"] = extracted.dmx_address
            else:
                payload["dmx"] = {"address": extracted.dmx_address}

        return SemanticObject(
            object_type="fixture",
            properties=payload,
            confidence=0.75,
            source_offsets=tuple(value.offset for value in cluster.values),
        )

    def correlate(self, values: Iterable[ValueCluster]) -> list[SemanticObject]:
        """Build semantic objects from value clusters.

        Each cluster is converted into a SemanticObject. When a cluster contains
        a UUID and a string, the object is tagged as a fixture and carries the
        UUID and the first string as properties.
        """
        results: list[SemanticObject] = []

        for cluster in values:
            properties = self._extractor.extract(cluster)

            if properties.uuid is not None and properties.name is not None:
                results.append(self._build_fixture(cluster, properties))
            else:
                results.append(self._build_unknown(cluster))

        return results
