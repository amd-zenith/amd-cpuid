"""
Command-line tool to interpret AMD CPUID representations into a description.
"""

import argparse
import sys
from collections.abc import Sequence

from .cpuid import AmdCpuId


def _int(value: str) -> int:
    """Parse an integer accepting decimal, ``0x`` hex, ``0o`` octal, ``0b`` bin."""
    try:
        return int(value, 0)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid integer value: {value!r}")


def describe(cpu: AmdCpuId) -> str:
    """Render a multi-line, human-readable description of a CPUID identity."""
    lines = [
        f"Description:        {cpu.description}",
        f"Family name:        {cpu.familyname}",
        f"Microarchitecture:  {cpu.microarchitecture}",
        f"Codename:           {cpu.codename}",
        f"Family:             {cpu.family:#04x} ({cpu.family})",
        f"Model:              {cpu.model:#04x} ({cpu.model})",
        f"Stepping:           {cpu.stepping:#03x} ({cpu.stepping})",
        "Fields:",
        f"  Base family:      {cpu.familybase:#x}",
        f"  Extended family:  {cpu.familyext:#x}",
        f"  Base model:       {cpu.modelbase:#x}",
        f"  Extended model:   {cpu.modelext:#x}",
        "Signatures:",
        f"  CPUID leaf 1 EAX: {cpu.cpuid_signature:#010x}",
        f"  Microcode header: {cpu.ucode_signature:#06x}",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="amd_cpuid", description="Interpret AMD CPUID representations into a description.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-c", "--cpuid", metavar="EAX", type=_int, help="standard CPUID instruction signature (e.g. 0x00A00F00)")
    group.add_argument("-u", "--ucode", metavar="SIG", type=_int, help="AMD microcode patch header cpuid field (e.g. 0xA000)")
    group.add_argument("-f", "--fms", nargs=3, metavar=("FAMILY", "MODEL", "STEPPING"), type=_int, help="display family, model and stepping (e.g. 0x19 0x00 0x0)")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        if args.cpuid is not None:
            cpu = AmdCpuId.from_cpuid_signature(args.cpuid)
        elif args.ucode is not None:
            cpu = AmdCpuId.from_ucode_signature(args.ucode)
        else:
            family, model, stepping = args.fms
            cpu = AmdCpuId.from_fms(family, model, stepping)
    except (ValueError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(describe(cpu))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
