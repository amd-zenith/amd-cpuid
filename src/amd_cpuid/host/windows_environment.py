"""
Read the CPUID identity of the running processor on Windows, from the
``PROCESSOR_IDENTIFIER`` environment variable.

Windows sets it for every process from the registry, e.g.
``"AMD64 Family 25 Model 33 Stepping 2, AuthenticAMD"``. Whoever starts the
process can change it, so :mod:`.windows_registry` is preferred.
"""

import os

from ..cpuid import AmdCpuId
from ._windows import parse_identifier


def read_cpuid() -> AmdCpuId:
    """
    Return the identity of the running processor.

    Raises :class:`OSError` when ``PROCESSOR_IDENTIFIER`` is not set, and
    :class:`ValueError` when the processor is not an AMD one.
    """
    value = os.environ.get("PROCESSOR_IDENTIFIER")
    if value is None:
        raise OSError("the PROCESSOR_IDENTIFIER environment variable is not set")

    # The vendor follows the last comma.
    identifier, _, vendor = value.rpartition(",")
    vendor = vendor.strip()
    if vendor != "AuthenticAMD":
        raise ValueError(f"not an AMD processor (PROCESSOR_IDENTIFIER {value!r})")
    return parse_identifier(identifier)
