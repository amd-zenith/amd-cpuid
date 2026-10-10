"""
Read the CPUID identity of the running processor on Windows, from the registry.

Windows stores the family, model and stepping it decoded from the ``CPUID``
instruction under ``HKEY_LOCAL_MACHINE\\HARDWARE\\DESCRIPTION\\System\\CentralProcessor``,
which any user can read.
"""

try:
    import winreg
except ImportError:  # not running on Windows
    winreg = None

from ..cpuid import AmdCpuId
from ._windows import parse_identifier

_KEY = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"


def read_cpuid() -> AmdCpuId:
    """
    Return the identity of the running processor.

    Only the first processor is read, as the cores of a system normally share
    the same family, model and stepping. Raises :class:`OSError` when the
    registry cannot be read, and :class:`ValueError` when the processor is not
    an AMD one.
    """
    if winreg is None:
        raise OSError("the Windows registry is not available on this system")
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _KEY) as key:
        vendor, _ = winreg.QueryValueEx(key, "VendorIdentifier")
        identifier, _ = winreg.QueryValueEx(key, "Identifier")

    if vendor != "AuthenticAMD":
        raise ValueError(f"not an AMD processor (VendorIdentifier {vendor!r})")
    return parse_identifier(identifier)
