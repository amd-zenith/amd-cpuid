"""
AMD CPU microarchitecture enumeration.
"""

from enum import Enum


class Microarchitecture(str, Enum):
    """AMD CPU microarchitecture, resolved from a ``(family, model)`` pair.

    Each member's value is its human-readable display name (e.g. ``"Zen 2"``).
    The enum subclasses :class:`str`, so a member compares equal to and formats
    as its display name, and can be used anywhere the plain string was before.
    """

    K8 = "K8"
    K10 = "K10"
    BOBCAT = "Bobcat"
    BULLDOZER = "Bulldozer"
    PILEDRIVER = "Piledriver"
    STEAMROLLER = "Steamroller"
    EXCAVATOR = "Excavator"
    JAGUAR = "Jaguar"
    PUMA = "Puma"
    ZEN = "Zen"
    ZEN2 = "Zen 2"
    ZEN3 = "Zen 3"
    ZEN4 = "Zen 4"
    ZEN5 = "Zen 5"
    ZEN6 = "Zen 6"

    #: The ``(family, model)`` pair is not covered by any known range.
    UNKNOWN = "Unknown"

    def __str__(self) -> str:
        # Keep formatting identical across Python versions and to the old bare
        # string (f-strings, str(), "%s" all yield the display name).
        return self.value
