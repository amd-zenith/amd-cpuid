"""
AMD CPU microarchitecture lookup by ``(family, model)`` range.
"""

from ..microarchitecture import Microarchitecture


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
