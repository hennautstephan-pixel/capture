"""
Knowledge decoder registry builder.

Centralises the registration of every decoder used by the
knowledge engine.
"""

from __future__ import annotations

from capture_recovery.knowledge.registry import (
    DecoderRegistry,
)

from capture_recovery.knowledge.decoders.fixture_decoder import (
    FixtureDecoder,
)


# ----------------------------------------------------------------------
# Future imports
#
# from capture_recovery.knowledge.decoders.universe_decoder import (
#     UniverseDecoder,
# )
#
# from capture_recovery.knowledge.decoders.group_decoder import (
#     GroupDecoder,
# )
#
# from capture_recovery.knowledge.decoders.scene_decoder import (
#     SceneDecoder,
# )
# ----------------------------------------------------------------------


class RegistryBuilder:
    """
    Builds a fully configured DecoderRegistry.
    """

    def __init__(self) -> None:
        self.registry = DecoderRegistry()

    # ------------------------------------------------------------------

    def register_builtin(self) -> "RegistryBuilder":
        """
        Register every built-in decoder.
        """

        self.registry.register(
            FixtureDecoder(),
        )

        #
        # Future registrations
        #
        # self.registry.register(
        #     UniverseDecoder(),
        # )
        #
        # self.registry.register(
        #     GroupDecoder(),
        # )
        #
        # self.registry.register(
        #     SceneDecoder(),
        # )

        return self

    # ------------------------------------------------------------------

    def build(self) -> DecoderRegistry:
        """
        Return the configured registry.
        """

        return self.registry


# ----------------------------------------------------------------------


def build_default_registry() -> DecoderRegistry:
    """
    Build the default decoder registry.
    """

    return (
        RegistryBuilder()
        .register_builtin()
        .build()
    )