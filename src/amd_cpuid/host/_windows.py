"""
Parse the processor identifier Windows reports, shared by the Windows backends.
"""

import re

from ..cpuid import AmdCpuId

#: Windows decodes the display family, model and stepping from the ``CPUID``
#: instruction, e.g. ``"AMD64 Family 25 Model 33 Stepping 2"``.
_IDENTIFIER = re.compile(r"\bFamily (\d+) Model (\d+) Stepping (\d+)\b")


def parse_identifier(identifier: str) -> AmdCpuId:
    """
    Build from a Windows processor identifier, e.g. ``"AMD64 Family 25 Model 33 Stepping 2"``.

    Raises :class:`ValueError` when it holds no family, model and stepping.
    """
    match = _IDENTIFIER.search(identifier)
    if match is None:
        raise ValueError(f"invalid processor identifier: {identifier!r}")
    family, model, stepping = (int(group) for group in match.groups())
    return AmdCpuId.from_fms(family, model, stepping)
