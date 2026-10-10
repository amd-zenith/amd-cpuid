from unittest import mock

import pytest

from amd_cpuid import AmdCpuId, system
from amd_cpuid.host import linux_cpuid, linux_cpuinfo


ZEN3 = AmdCpuId.from_fms(0x19, 0x21, 0x2)


def _fail(exc):
    return mock.Mock(side_effect=exc)


def test_system_uses_first_backend():
    with mock.patch.object(linux_cpuinfo, "read_cpuid", return_value=ZEN3), \
         mock.patch.object(linux_cpuid, "read_cpuid") as device:
        assert system.read_cpuid() == ZEN3
    device.assert_not_called()


def test_system_falls_back_when_backend_unreadable():
    with mock.patch.object(linux_cpuinfo, "read_cpuid", _fail(FileNotFoundError("no /proc"))), \
         mock.patch.object(linux_cpuid, "read_cpuid", return_value=ZEN3):
        assert system.read_cpuid() == ZEN3


def test_system_reports_every_backend_error():
    with mock.patch.object(linux_cpuinfo, "read_cpuid", _fail(FileNotFoundError("no /proc"))), \
         mock.patch.object(linux_cpuid, "read_cpuid", _fail(PermissionError("not root"))):
        with pytest.raises(OSError, match="no /proc; not root"):
            system.read_cpuid()


def test_system_does_not_fall_back_for_other_vendors():
    with mock.patch.object(linux_cpuinfo, "read_cpuid", _fail(ValueError("not an AMD processor"))), \
         mock.patch.object(linux_cpuid, "read_cpuid") as device:
        with pytest.raises(ValueError, match="not an AMD processor"):
            system.read_cpuid()
    device.assert_not_called()
