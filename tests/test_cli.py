from unittest import mock

import amd_cpuid
from amd_cpuid import AmdCpuId, cli, system


def test_read_cpuid_exported_at_library_level():
    assert amd_cpuid.read_cpuid is system.read_cpuid


def test_cli_local(capsys):
    with mock.patch.object(cli, "read_cpuid", return_value=AmdCpuId.from_fms(0x19, 0x21, 0x2)):
        assert cli.main(["--local"]) == 0
    out, err = capsys.readouterr()
    assert "Description:        Zen 3, Vermeer" in out
    assert err == ""


def test_cli_local_unreadable(capsys):
    with mock.patch.object(cli, "read_cpuid", side_effect=OSError("cannot read the CPUID")):
        assert cli.main(["-l"]) == 2
    assert capsys.readouterr().err == "Error: cannot read the CPUID\n"


def test_cli_local_other_vendor(capsys):
    with mock.patch.object(cli, "read_cpuid", side_effect=ValueError("not an AMD processor")):
        assert cli.main(["-l"]) == 2
    assert capsys.readouterr().err == "Error: not an AMD processor\n"
