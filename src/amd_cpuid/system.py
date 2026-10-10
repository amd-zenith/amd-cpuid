"""
Read the CPUID identity of the processor this code is running on.

Callers do not need to know where it comes from: each backend in :mod:`.host`
is tried in turn until one can be read.
"""

from .cpuid import AmdCpuId
from .host import linux_cpuid, linux_cpuinfo, windows_environment, windows_registry

#: Tried in order. ``/proc/cpuinfo`` goes first because any user can read it, and
#: the registry before ``PROCESSOR_IDENTIFIER`` because the latter can be overridden.
_BACKENDS = (linux_cpuinfo, linux_cpuid, windows_registry, windows_environment)


def read_cpuid() -> AmdCpuId:
    """
    Return the identity of the running processor.

    Raises :class:`OSError` when no backend can be read, and :class:`ValueError`
    when the processor is not an AMD one.
    """
    errors = []
    for backend in _BACKENDS:
        try:
            return backend.read_cpuid()
        except OSError as exc:
            errors.append(str(exc))
    raise OSError("cannot read the CPUID of this processor: " + "; ".join(errors))
