"""
Read the CPUID identity of the running processor on Linux, from ``/dev/cpu/0/cpuid``.

The kernel ``cpuid`` driver executes the ``CPUID`` instruction and returns the
raw registers. The device is usually readable by root only, and needs the
``cpuid`` kernel module when the driver is not built into the kernel.
"""

from ..cpuid import AmdCpuId


def read_cpuid() -> AmdCpuId:
    """
    Return the identity of the running processor.

    Raises :class:`OSError` when ``/dev/cpu/0/cpuid`` cannot be read, and
    :class:`ValueError` when the processor is not an AMD one.
    """
    # The file position is the CPUID leaf, and each 16-byte read returns the
    # eax, ebx, ecx and edx registers (little-endian) then moves to the next leaf.
    with open("/dev/cpu/0/cpuid", "rb", buffering=0) as device:
        leaf0 = device.read(16)
        leaf1 = device.read(16)

    # Leaf 0 spells the vendor across ebx, edx and ecx.
    vendor = (leaf0[4:8] + leaf0[12:16] + leaf0[8:12]).decode("ascii", "replace")
    if vendor != "AuthenticAMD":
        raise ValueError(f"not an AMD processor (vendor {vendor!r})")
    # Leaf 1 eax is the CPUID signature.
    return AmdCpuId.from_cpuid_signature(int.from_bytes(leaf1[0:4], "little"))
