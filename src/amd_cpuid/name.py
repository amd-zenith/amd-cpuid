"""
AMD Zen processor codename lookup.
"""

from .microarchitecture import Microarchitecture

#: Returned by the lookup helpers when nothing matches.
UNKNOWN = "Unknown"


# Family-level names.
#
# Compiled from:
#   - https://en.wikipedia.org/wiki/List_of_AMD_CPU_microarchitectures
#   - https://en.wikipedia.org/wiki/AMD_10h#11h
#   - Linux kernel arch/x86/include/asm/cpu_device_id.h and
#     arch/x86/kernel/cpu/amd.c (Zen family/model ranges)
#   - Todd Allen's cpuid synth table (https://www.etallen.com/cpuid.html)
_FAMILY_NAMES: dict[int, str] = {
    0x0f: "K8",
    0x10: "K10",
    0x11: "Turion",
    0x12: "Fusion",
    0x14: "Bobcat",
    0x15: "Bulldozer",
    0x16: "Jaguar/Puma",
    0x17: "Zen/Zen+/Zen2",
    0x19: "Zen3/Zen3+/Zen4",
    0x1a: "Zen5/Zen6",
}

def lookup_family_name(family: int) -> str:
    """
    Return the AMD codename for the given extended family number.
    This is based on marketing materials and Linux kernel source, and is not guaranteed to be complete.
    Returns ``"Unknown"`` when the family is not known.
    """
    return _FAMILY_NAMES.get(family, UNKNOWN)

# Microarchitecture by ``(family, model)`` range.
#
# The Zen generations (families 0x17 / 0x19 / 0x1a) are reproduced verbatim from
# the Linux kernel "Figure out Zen generations" switch in
# https://github.com/torvalds/linux/blob/master/arch/x86/kernel/cpu/amd.c
# The kernel folds Zen+ into Zen, and the area-optimised "c" cores (Zen 4c,
# Zen 5c) into their base generation, so those refinements are not distinguished
# here. Note the kernel does not classify family 0x17 models 0x80-0x8f.
#
# Pre-Zen families come from the WikiChip CPUID table (microarchitecture column
# and "BD vN" range annotations), Dec 2025 snapshot via the Wayback Machine:
#   https://web.archive.org/web/20251208232456/https://en.wikichip.org/wiki/amd/cpuid
# cross-checked with
#   https://en.wikipedia.org/wiki/List_of_AMD_CPU_microarchitectures
# Family 0x11 (Griffin) uses K8 cores and family 0x12 (Llano) uses K10 cores.
#
# Each value is a tuple of inclusive ``(model_lo, model_hi, microarchitecture)``
# ranges; a model outside every range resolves to ``Microarchitecture.UNKNOWN``.
_MICROARCH_RANGES: dict[int, tuple[tuple[int, int, Microarchitecture], ...]] = {
    0x0f: ((0x00, 0xff, Microarchitecture.K8),),
    0x10: ((0x00, 0xff, Microarchitecture.K10),),
    0x11: ((0x00, 0xff, Microarchitecture.K8),),  # Griffin (K8 "Hound" cores)
    0x12: ((0x00, 0xff, Microarchitecture.K10),),  # Llano (K10 "Husky" cores)
    0x14: ((0x00, 0xff, Microarchitecture.BOBCAT),),
    0x15: (
        (0x00, 0x01, Microarchitecture.BULLDOZER),
        (0x02, 0x02, Microarchitecture.PILEDRIVER),
        (0x10, 0x1f, Microarchitecture.PILEDRIVER),
        (0x30, 0x3f, Microarchitecture.STEAMROLLER),
        (0x60, 0x7f, Microarchitecture.EXCAVATOR),
    ),
    0x16: (
        (0x00, 0x0f, Microarchitecture.JAGUAR),
        (0x30, 0x3f, Microarchitecture.PUMA),
    ),
    0x17: (  # kernel amd.c case 0x17
        (0x00, 0x2f, Microarchitecture.ZEN),
        (0x50, 0x5f, Microarchitecture.ZEN),
        (0x30, 0x4f, Microarchitecture.ZEN2),
        (0x60, 0x7f, Microarchitecture.ZEN2),
        (0x90, 0x91, Microarchitecture.ZEN2),
        (0xa0, 0xaf, Microarchitecture.ZEN2),
        # The kernel leaves the remaining family-0x17 models (e.g. 0x80-0x8f)
        # unclassified, but the whole family shares the Zen1/Zen2 microcode ISA.
        # This trailing catch-all keeps the family exhaustive so no valid Zen
        # patch is left unrecognized (e.g. model 0x84); it is reached only for
        # models not matched by the specific ranges above.
        (0x00, 0xff, Microarchitecture.ZEN2),
    ),
    0x19: (  # kernel amd.c case 0x19
        (0x00, 0x0f, Microarchitecture.ZEN3),
        (0x20, 0x5f, Microarchitecture.ZEN3),
        (0x10, 0x1f, Microarchitecture.ZEN4),
        (0x60, 0xaf, Microarchitecture.ZEN4),
    ),
    0x1a: (  # kernel amd.c case 0x1a
        (0x00, 0x2f, Microarchitecture.ZEN5),
        (0x40, 0x4f, Microarchitecture.ZEN5),
        (0x60, 0x7f, Microarchitecture.ZEN5),
        (0x50, 0x5f, Microarchitecture.ZEN6),
        (0x80, 0xaf, Microarchitecture.ZEN6),
        (0xc0, 0xef, Microarchitecture.ZEN6),
    ),
}

def lookup_microarch_name(family: int, model: int) -> Microarchitecture:
    """
    Return the microarchitecture for a ``(family, model)`` pair.
    Returns ``Microarchitecture.UNKNOWN`` when the pair is not covered by any
    known range. The returned value is a :class:`str` subclass, so it still
    compares equal to and formats as its display name (e.g. ``"Zen 2"``).
    """
    for model_lo, model_hi, microarch in _MICROARCH_RANGES.get(family, ()):
        if model_lo <= model <= model_hi:
            return microarch
    return Microarchitecture.UNKNOWN

# Per-model processor codenames, keyed by ``(family, model)``.
#
# Each model is mapped from the documented product-line ranges, so an early or
# engineering stepping (model ``0xN0``) shares the production codename of its
# range. Codenames verified against:
#   - https://web.archive.org/web/20251208232456/https://en.wikichip.org/wiki/amd/cpuid
#   - https://en.wikipedia.org/wiki/List_of_AMD_CPU_microarchitectures
#   - Linux kernel arch/x86/kernel/cpu/amd.c (Zen family/model ranges)
_CODENAMES: dict[tuple[int, int], str] = {
    # Family 0x10 (K10)
    (0x10, 0x02): "Barcelona/Agena",
    (0x10, 0x04): "Shanghai",
    (0x10, 0x08): "Istanbul/Lisbon",
    (0x10, 0x0a): "Thuban/Zosma",
    # Family 0x11 (Turion / Puma platform)
    (0x11, 0x03): "Griffin",
    # Family 0x12 (Fusion)
    (0x12, 0x00): "Llano",
    (0x12, 0x01): "Llano",
    # Family 0x14 (Bobcat)
    (0x14, 0x00): "Ontario/Zacate",
    (0x14, 0x01): "Ontario/Zacate",
    (0x14, 0x02): "Ontario/Zacate",
    # Family 0x15 (Bulldozer / Piledriver / Steamroller / Excavator)
    (0x15, 0x00): "Zambezi",  # Bulldozer (0x00-0x0F, except 0x02)
    (0x15, 0x01): "Zambezi",
    (0x15, 0x02): "Vishera",  # Piledriver
    (0x15, 0x10): "Trinity",  # Piledriver (0x10-0x1F)
    (0x15, 0x30): "Kaveri",  # Steamroller (0x30-0x3F)
    (0x15, 0x60): "Carrizo",  # Excavator (0x60-0x6F)
    (0x15, 0x70): "Stoney Ridge",  # Excavator (0x70-0x7F)
    # Family 0x16 (Jaguar / Puma)
    (0x16, 0x00): "Kabini/Temash",  # Jaguar (0x00-0x0F)
    (0x16, 0x30): "Beema/Mullins",  # Puma (0x30-0x3F)
    # Family 0x17 (Zen / Zen+ / Zen2)
    (0x17, 0x00): "Naples/Summit Ridge",  # Zeppelin (0x0X)
    (0x17, 0x01): "Naples/Summit Ridge",
    (0x17, 0x08): "Pinnacle Ridge",
    (0x17, 0x11): "Raven Ridge",
    (0x17, 0x18): "Picasso",
    (0x17, 0x20): "Dali",
    (0x17, 0x30): "Rome/Castle Peak",  # 0x30-0x3F
    (0x17, 0x31): "Rome/Castle Peak",
    (0x17, 0x60): "Renoir",  # 0x60-0x67
    (0x17, 0x68): "Lucienne",  # 0x68-0x6F
    (0x17, 0x70): "Matisse",  # 0x70-0x7F
    (0x17, 0x71): "Matisse",
    (0x17, 0x90): "Van Gogh",  # 0x90-0x97
    (0x17, 0x91): "Van Gogh",
    (0x17, 0xa0): "Mendocino",  # 0xA0-0xAF
    # Family 0x19 (Zen3 / Zen3+ / Zen4)
    (0x19, 0x00): "Milan",  # 0x00-0x0F (Chagall at 0x08)
    (0x19, 0x01): "Milan",
    (0x19, 0x08): "Chagall",
    (0x19, 0x10): "Genoa",  # 0x10-0x1F (Storm Peak at 0x18)
    (0x19, 0x11): "Genoa",
    (0x19, 0x18): "Storm Peak",
    (0x19, 0x20): "Vermeer",  # 0x20-0x2F
    (0x19, 0x21): "Vermeer",
    (0x19, 0x40): "Rembrandt",  # 0x40-0x4F
    (0x19, 0x44): "Rembrandt",
    (0x19, 0x50): "Cezanne/Barcelo",  # 0x50-0x5F
    (0x19, 0x60): "Raphael",  # 0x60-0x6F
    (0x19, 0x61): "Raphael",
    (0x19, 0x70): "Phoenix",  # 0x70-0x77 (Hawk Point refresh)
    (0x19, 0x74): "Phoenix",
    (0x19, 0x75): "Phoenix",
    (0x19, 0x78): "Phoenix 2",  # 0x78-0x7F
    (0x19, 0x7c): "Phoenix 2",
    (0x19, 0xa0): "Bergamo/Siena",  # 0xA0-0xAF (Zen4c)
    # Family 0x1a (Zen5 / Zen6)
    (0x1a, 0x00): "Turin",  # 0x00-0x02
    (0x1a, 0x01): "Turin",
    (0x1a, 0x02): "Turin",
    (0x1a, 0x08): "Shimada Peak",  # 0x08-0x0F (Zen5 Threadripper)
    (0x1a, 0x10): "Turin Dense",  # 0x10-0x1F (Zen5c)
    (0x1a, 0x11): "Turin Dense",
    (0x1a, 0x24): "Strix Point",  # 0x20-0x2F
    (0x1a, 0x44): "Granite Ridge",  # 0x44-0x4F
    (0x1a, 0x60): "Krackan Point",  # 0x60-0x67
    (0x1a, 0x68): "Krackan Point 2",  # 0x68-0x6F
    (0x1a, 0x70): "Strix Halo",  # 0x70-0x7F
}


def lookup_codename(family: int, model: int) -> str:
    """Return the marketing codename for a ``(family, model)`` pair.

    For example ``"Matisse"``. Returns ``"Unknown"`` when the model is not in
    the table.
    """
    return _CODENAMES.get((family, model), UNKNOWN)
