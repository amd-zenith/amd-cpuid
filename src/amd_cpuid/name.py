"""
AMD Zen processor codename lookup.
"""

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
    """Return the AMD codename for the given extended family number."""
    return _FAMILY_NAMES.get(family, "Unknown")
