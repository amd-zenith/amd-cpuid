from amd_cpuid import AmdCpuId


def test_microarchitecture_is_str_compatible():
    # The enum subclasses str, so existing string-based callers keep working.
    micro = AmdCpuId.from_fms(0x17, 0x71, 0x0).microarchitecture
    assert isinstance(micro, str)
    assert micro == "Zen 2"
    assert f"{micro}" == "Zen 2"
    assert str(micro) == "Zen 2"
