"""
Read the CPUID identity of the processor this code is running on.

Use :func:`amd_cpuid.system.read_cpuid`, which picks a backend for you. Each
module here reads it from a different source:

- :mod:`.linux_cpuinfo`: Linux ``/proc/cpuinfo``, readable by any user.
- :mod:`.linux_cpuid`: Linux ``/dev/cpu/0/cpuid``, usually readable by root only.
"""
