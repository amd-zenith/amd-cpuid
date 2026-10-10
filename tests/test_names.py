from amd_cpuid import (
    AmdCpuId,
    Microarchitecture,
    lookup_family_name,
    lookup_microarch_name,
)


def test_unknown_family_name():
    # 0x13 is a gap AMD never shipped, so it has no codename.
    assert lookup_family_name(0x13) == "Unknown"
    assert AmdCpuId.from_fms(0x13, 0x00, 0x0).familyname == "Unknown"


def test_microarch_lookup_examples():
    assert lookup_microarch_name(0x17, 0x71) == "Zen 2"
    assert lookup_microarch_name(0x19, 0x21) == "Zen 3"
    assert lookup_microarch_name(0x1A, 0x44) == "Zen 5"
    assert AmdCpuId.from_fms(0x19, 0x21, 0x0).microarchitecture is Microarchitecture.ZEN3


def test_family_0x17_catch_all_resolves_undocumented_model():
    # Family 0x17 model 0x84 (real patch cpuid00880F40) is outside the kernel's
    # specific model ranges, but the whole family shares the Zen1/Zen2 ISA, so
    # the exhaustive catch-all resolves it to Zen 2 rather than "Unknown".
    cpu = AmdCpuId.from_fms(0x17, 0x84, 0x5)
    assert cpu.microarchitecture is Microarchitecture.ZEN2
    assert cpu.microarchitecture != Microarchitecture.UNKNOWN


def test_unknown_microarch_for_unmapped_model():
    # An unmapped family (0x18 was never shipped) has no microarch range.
    assert AmdCpuId.from_fms(0x18, 0x00, 0x0).microarchitecture is Microarchitecture.UNKNOWN
