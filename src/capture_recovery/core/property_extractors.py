from __future__ import annotations

from dataclasses import dataclass

from capture_recovery.core.recovered_value import RecoveredValue
from capture_recovery.core.value_clusterer import ValueCluster


@dataclass(frozen=True, slots=True)
class FixtureProperties:
    """Represents the properties that can be extracted from a fixture cluster."""

    uuid: str | None
    """The UUID value extracted from the cluster, if any."""

    name: str | None
    """The first string value extracted from the cluster, if any."""

    dmx_universe: int | None
    """The DMX universe value extracted from the cluster, if any."""

    dmx_address: int | None
    """The DMX address value extracted from the cluster, if any."""


class FixturePropertyExtractor:
    """Extract fixture-related properties from a value cluster.

    This helper centralizes the current search logic for UUIDs, names, and DMX
    values without constructing semantic objects.
    """

    def _find_uuid(self, cluster: ValueCluster) -> RecoveredValue | None:
        """Return the first UUID value found in the cluster, if any."""
        for value in cluster.values:
            if value.type == "uuid":
                return value
        return None

    def _find_name(self, cluster: ValueCluster) -> RecoveredValue | None:
        """Return the first string value found in the cluster, if any."""
        for value in cluster.values:
            if value.type == "string":
                return value
        return None

    def _find_universe(self, cluster: ValueCluster) -> RecoveredValue | None:
        """Return the first integer that looks like a DMX universe."""
        for value in cluster.values:
            if value.type != "int":
                continue
            if isinstance(value.value, int) and 1 <= value.value <= 256:
                return value
        return None

    def _find_address(self, cluster: ValueCluster) -> RecoveredValue | None:
        """Return the first integer that looks like a DMX address."""
        universe = self._find_universe(cluster)
        for value in cluster.values:
            if value.type != "int":
                continue
            if not isinstance(value.value, int):
                continue
            if 1 <= value.value <= 512 and (universe is None or value.value != universe.value):
                return value
        return None

    def extract(self, cluster: ValueCluster) -> FixtureProperties:
        """Extract the fixture properties that are present in a cluster."""
        uuid_value = self._find_uuid(cluster)
        name_value = self._find_name(cluster)
        universe_value = self._find_universe(cluster)
        address_value = self._find_address(cluster)

        return FixtureProperties(
            uuid=uuid_value.value if uuid_value is not None else None,
            name=name_value.value if name_value is not None else None,
            dmx_universe=universe_value.value if universe_value is not None else None,
            dmx_address=address_value.value if address_value is not None else None,
        )


__all__ = ["FixtureProperties", "FixturePropertyExtractor"]
