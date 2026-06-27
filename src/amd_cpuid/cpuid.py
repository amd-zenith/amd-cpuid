"""
Parse, interpret and convert between AMD CPUID representations.
"""

from dataclasses import dataclass
from .name import lookup_family_name


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
