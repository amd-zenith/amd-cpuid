"""
Parse, interpret and convert between AMD CPUID representations.
"""

from dataclasses import dataclass
from .microarchitecture import Microarchitecture
from .name import (
    UNKNOWN,
    lookup_codename,
    lookup_family_name,
    lookup_microarch_name,
)


@dataclass(frozen=True)
class AmdCpuId:
    family: int
    model: int
    stepping: int

    @classmethod
    def from_ucode_signature(cls, value: int) -> "AmdCpuId":
        """
        Build from an AMD microcode patch header ``cpuid`` field.
        Layout (low to high): ``stepping:4 model:4 extmodel:4 extfam:4 pad:16``.
        """
        stepping = value & 0xF
        modelbase = (value >> 4) & 0xF
        modelext = (value >> 8) & 0xF
        famext = (value >> 12) & 0xF
        #: AMD Zen processors always report a base family of ``0xF``
        return cls(
            family = 0xF + famext,
            model = (modelext << 4) | modelbase,
            stepping = stepping,
        )

    @classmethod
    def from_cpuid_signature(cls, value: int) -> "AmdCpuId":
        """
        Build from a standard ``CPUID`` leaf 1 ``EAX`` signature.
        Layout: ``stepping:4 model:4 family:4 type:2 _:2 extmodel:4 extfam:8``.
        """
        stepping = value & 0xF
        modelbase = (value >> 4) & 0xF
        fambase = (value >> 8) & 0xF
        modelext = (value >> 16) & 0xF
        famext = (value >> 20) & 0xFF
        return cls(
            family = fambase + famext,
            model = (modelext << 4) | modelbase,
            stepping = stepping,
        )

    @classmethod
    def from_fms(cls, family: int, model: int, stepping: int) -> "AmdCpuId":
        """
        Build from family, model and stepping values.
        """
        return cls(
            family = family,
            model = model,
            stepping = stepping,
        )

    @property
    def familybase(self) -> int:
        """The base family number (the family field, capped at ``0xF``)."""
        return min(self.family, 0xF)

    @property
    def familyext(self) -> int:
        """The extended family number (the family above the base family)."""
        return max(self.family - 0xF, 0)

    @property
    def familyname(self) -> str:
        """The family name (e.g. ``"Zen3/Zen4"``)."""
        return lookup_family_name(self.family)

    @property
    def microarchitecture(self) -> Microarchitecture:
        """
        The microarchitecture (e.g. ``Microarchitecture.ZEN2``), from family/model ranges.

        The result is a :class:`str` subclass, so it still compares equal to and
        formats as its display name (e.g. ``"Zen 2"``).
        """
        return lookup_microarch_name(self.family, self.model)

    @property
    def codename(self) -> str:
        """The processor codename (e.g. ``"Matisse"``), or ``"Unknown"``."""
        return lookup_codename(self.family, self.model)

    @property
    def fms(self) -> str:
        """The numeric identity, e.g. ``"Family 0x19, Model 0x21, Stepping 0"``."""
        return f"Family 0x{self.family:02X}, Model 0x{self.model:02X}, Stepping {self.stepping}"

    @property
    def description(self) -> str:
        """
        A short human-readable description, e.g. ``"Zen 3, Vermeer"``.

        This is the microarchitecture -- falling back to the family name when the
        microarchitecture is unknown (so an undocumented model still names its
        family, e.g. ``"Bulldozer"``) -- followed by the codename, when one is
        known.
        """
        micro = self.microarchitecture
        head = self.familyname if micro is Microarchitecture.UNKNOWN else str(micro)
        codename = self.codename
        if codename == UNKNOWN:
            return head
        return f"{head}, {codename}"

    @property
    def modelbase(self) -> int:
        """The base model number (the low nibble of the model)."""
        return self.model & 0xF

    @property
    def modelext(self) -> int:
        """The extended model number (the high nibble of the model)."""
        return (self.model >> 4) & 0xF

    @property
    def ucode_signature(self) -> int:
        """
        Re-encode as an AMD microcode patch header ``cpuid`` field.
        Layout (low to high): ``stepping:4 model:4 extmodel:4 extfam:4 pad:16``.
        """
        return (
            (self.stepping & 0xF)
            | ((self.modelbase & 0xF) << 4)
            | ((self.modelext & 0xF) << 8)
            | ((self.familyext & 0xF) << 12)
        )

    @property
    def cpuid_signature(self) -> int:
        """
        Re-encode as a standard ``CPUID`` instruction signature.
        Layout: ``stepping:4 model:4 family:4 type:2 _:2 extmodel:4 extfam:8``.
        """
        return (
            (self.stepping & 0xF)
            | ((self.modelbase & 0xF) << 4)
            | ((self.familybase & 0xF) << 8)
            | ((self.modelext & 0xF) << 16)
            | ((self.familyext & 0xFF) << 20)
        )

    def __str__(self) -> str:
        """One-line identity, e.g. ``"Family 0x19, Model 0x21, Stepping 0 (Zen 3, Vermeer)"``."""
        return f"{self.fms} ({self.description})"
