from unittest import mock

import pytest

from amd_cpuid import AmdCpuId
from amd_cpuid.host import linux_cpuid, linux_cpuinfo


RYZEN_5950X_CPUINFO = """\
processor\t: 0
vendor_id\t: AuthenticAMD
cpu family\t: 25
model\t\t: 33
model name\t: AMD Ryzen 9 5950X 16-Core Processor
stepping\t: 2
microcode\t: 0xa201205

processor\t: 1
vendor_id\t: AuthenticAMD
cpu family\t: 23
model\t\t: 113
stepping\t: 0
"""

INTEL_CPUINFO = """\
processor\t: 0
vendor_id\t: GenuineIntel
cpu family\t: 6
model\t\t: 158
stepping\t: 10
"""

# CPUID leaves 0 and 1 as read from /dev/cpu/0/cpuid: eax, ebx, ecx, edx each.
RYZEN_5950X_LEAVES = (
    (0x10).to_bytes(4, "little") + b"Auth" + b"cAMD" + b"enti"
    + (0x00A20F12).to_bytes(4, "little") + bytes(12)
)

INTEL_LEAVES = (
    (0x16).to_bytes(4, "little") + b"Genu" + b"ntel" + b"ineI"
    + (0x000906EA).to_bytes(4, "little") + bytes(12)
)


def _read_cpuid(module, path, data):
    """Call ``module.read_cpuid`` with ``data`` as the contents of ``path``."""
    with mock.patch.object(module, "open", mock.mock_open(read_data=data), create=True) as opened:
        cpu = module.read_cpuid()
    assert opened.call_args.args[0] == path
    return cpu


def test_linux_cpuinfo_reads_first_processor():
    cpu = _read_cpuid(linux_cpuinfo, "/proc/cpuinfo", RYZEN_5950X_CPUINFO)
    assert cpu == AmdCpuId.from_fms(0x19, 0x21, 0x2)


def test_linux_cpuinfo_rejects_other_vendors():
    with pytest.raises(ValueError, match="not an AMD processor"):
        _read_cpuid(linux_cpuinfo, "/proc/cpuinfo", INTEL_CPUINFO)


def test_linux_cpuid_reads_signature():
    cpu = _read_cpuid(linux_cpuid, "/dev/cpu/0/cpuid", RYZEN_5950X_LEAVES)
    assert cpu == AmdCpuId.from_fms(0x19, 0x21, 0x2)


def test_linux_cpuid_rejects_other_vendors():
    with pytest.raises(ValueError, match="not an AMD processor"):
        _read_cpuid(linux_cpuid, "/dev/cpu/0/cpuid", INTEL_LEAVES)


def test_linux_cpuinfo_on_this_machine():
    try:
        with open("/proc/cpuinfo", encoding="utf-8") as file:
            is_amd = "AuthenticAMD" in file.read()
    except OSError:
        is_amd = False
    if not is_amd:
        pytest.skip("not running Linux on an AMD processor")
    assert linux_cpuinfo.read_cpuid().family >= 0x0F


def test_linux_cpuid_on_this_machine_matches_cpuinfo():
    try:
        cpu = linux_cpuid.read_cpuid()
    except (OSError, ValueError) as exc:
        pytest.skip(f"cannot read /dev/cpu/0/cpuid: {exc}")
    assert cpu == linux_cpuinfo.read_cpuid()
