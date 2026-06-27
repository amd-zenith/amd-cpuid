import pytest

from amd_cpuid import AmdCpuId, lookup_family_name


def test_from_cpuid_signature_milan():
    cpu = AmdCpuId.from_cpuid_signature(0x00A00F00)
    assert cpu.family == 0x19
    assert cpu.model == 0x00
    assert cpu.stepping == 0
    assert cpu.familyname == "Zen3/Zen4"


def test_from_ucode_signature_matisse():
    cpu = AmdCpuId.from_ucode_signature(0x8700)
    assert cpu.family == 0x17
    assert cpu.model == 0x70
    assert cpu.familybase == 0xF
    assert cpu.familyext == 0x8
    assert cpu.modelbase == 0x0
    assert cpu.modelext == 0x7
    assert cpu.familyname == "Zen/Zen+/Zen2"


def test_from_fms_raphael():
    cpu = AmdCpuId.from_fms(0x19, 0x60, 0x1)
    assert cpu.familyext == 0xA
    assert cpu.modelext == 0x6
    assert cpu.familyname == "Zen3/Zen4"


@pytest.mark.parametrize(
    "family, model, stepping",
    [
        (0x17, 0x71, 0x0),  # Zen2
        (0x19, 0x61, 0x2),  # Zen4
        (0x1A, 0x44, 0x0),  # Zen5
        (0x0F, 0x00, 0x0),  # base family only
    ],
)
def test_round_trip_all_representations(family, model, stepping):
    cpu = AmdCpuId.from_fms(family, model, stepping)
    assert AmdCpuId.from_ucode_signature(cpu.ucode_signature) == cpu
    assert AmdCpuId.from_cpuid_signature(cpu.cpuid_signature) == cpu
    assert cpu.family == family
    assert cpu.model == model
    assert cpu.stepping == stepping


def test_family_split():
    cpu = AmdCpuId.from_fms(0x1A, 0x44, 0x0)
    assert cpu.familybase == 0xF
    assert cpu.familyext == 0xB
    assert cpu.modelbase == 0x4
    assert cpu.modelext == 0x4


def test_zen5_family_name():
    assert AmdCpuId.from_fms(0x1A, 0x00, 0x0).familyname == "Zen5"


def test_unknown_family_name():
    assert lookup_family_name(0x16) == "Unknown"
    assert AmdCpuId.from_fms(0x16, 0x00, 0x0).familyname == "Unknown"


def test_signature_examples():
    cpu = AmdCpuId.from_fms(0x19, 0x21, 0x2)
    assert cpu.cpuid_signature == 0x00A20F12
    assert cpu.ucode_signature == 0xA212
