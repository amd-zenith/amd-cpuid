"""
Read the CPUID identity of the running processor on Linux, from ``/proc/cpuinfo``.

The kernel reports the family, model and stepping it decoded from the ``CPUID``
instruction, so no privileges or kernel modules are needed.
"""

from ..cpuid import AmdCpuId


def read_cpuid() -> AmdCpuId:
    """
    Return the identity of the running processor.

    Only the first processor listed is read, as the cores of a system normally
    share the same family, model and stepping. Raises :class:`OSError` when
    ``/proc/cpuinfo`` cannot be read, and :class:`ValueError` when the processor
    is not an AMD one.
    """
    with open("/proc/cpuinfo", encoding="utf-8") as file:
        first_processor = file.read().split("\n\n", 1)[0]

    fields: dict[str, str] = {}
    for line in first_processor.splitlines():
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()

    vendor = fields.get("vendor_id")
    if vendor != "AuthenticAMD":
        raise ValueError(f"not an AMD processor (vendor_id {vendor!r})")
    return AmdCpuId.from_fms(int(fields["cpu family"]), int(fields["model"]), int(fields["stepping"]))
